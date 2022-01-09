import os
import sys
from hashlib import md5
from tempfile import gettempdir
from threading import Thread
from shutil import which

import sublime
import requests


# Adding packages directory to PATH, to import additional modules
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'packages')
if path not in sys.path:
    sys.path.append(path)

# Importing modules from `packages` directory
import cloudconvert


class Svg2PngConverter:
    """ Converts SVG files to PNG. Supported 2 modes: online and offline """

    # Define temporary directory where converted pictures will be stored
    TMP_DIR = os.path.join(gettempdir(), 'svg-viewer')

    # List of all API keys
    API_KEYS = []

    # Current API key
    API_KEY = None

    def __init__(self, settings, converters) -> None:
        """ Initialization of converter """

        # Setting variables for the further use
        self.settings = settings
        self.converters = converters

        # Disabling sandbox mode
        cloudconvert.configure(sandbox=False)

    def __load_api_keys(self) -> None:
        """ Loading API keys from remote source or local file """

        # Getting path to keys list
        keys_list = self.settings.get('online', {}).get('keys_list')

        # If local file shema is selected, loads keys from defined file
        if keys_list.startswith('file://'):
            with open(keys_list[7:]) as file:
                self.API_KEYS = file.readlines()

        # Else, loading keys from remote source, it is assumed that
        # the Internet connection has already been checked
        else:
            self.API_KEYS = requests.get(keys_list).text.split('\n')

        # Setting current API key, first of API keys list
        self.API_KEY = self.API_KEYS[0]

        # Updating cloudconvert with new API key
        cloudconvert.configure(api_key=self.API_KEY)

    def convert(self, input_file_name: str):
        """ Converts file from SVG to PNG. If the conversion was
            successful, it returns the path to the output file,
            otherwise `False` """

        # If file extension verifying is enabled
        if self.settings.get('verify_file_extension'):
            for extension in self.settings.get('extensions', []):
                if input_file_name.endswith(extension):
                    # Extension matches, can continue converting
                    break
            else:
                # Extensions do not matches, abort converting
                sublime.error_message('Current file has a different extension from SVG! Define this extension or disable extension verifying in settings')
                return False

        # Create temporary directory
        os.makedirs(self.TMP_DIR, exist_ok=True)

        # Generating path output file, by hashing path to the origin file with md5
        output_file_name = md5(input_file_name.encode('utf-8')).hexdigest() + '.png'
        output_path = os.path.join(self.TMP_DIR, output_file_name)

        # Checking network connection, if connection was not established, raises exception
        try:
            # Raise exception, if offline mode is enabled
            if self.settings.get('force_offline_mode'):
                raise Exception()

            # Checks network connection
            requests.get('https://api.cloudconvert.com')

            # Connection was established, load API keys if this has not already been done
            if self.API_KEYS == []:
                self.__load_api_keys()

        except (requests.exceptions.ConnectionError, Exception):
            # Exception was raised, converting in offline mode
            result = self.convert_offline(input_file_name, output_path)
        else:
            # Exception was not raised, converting in online mode
            result = self.convert_online(input_file_name, output_path)

        # Returns path to output file or `False`
        return result and output_path

    def convert_online(self, input_file_name: str, output_file_name: str) -> bool:
        """ Converts file from SVG to PNG by cloudconvert.com service """

        # Getting settings for the further use
        engine = self.settings.get('online', {}).get('engine')
        dpi = self.settings.get('dpi')

        # Сhecks the converter for supportability
        if engine not in ['imagemagick', 'inkscape', 'chrome', 'graphicsmagick', 'rsvg']:
            sublime.error_message('"{}" converter not supported. Please choose converter only from suggested list!'.format(engine))
            return False

        last_api_key = self.API_KEYS[(self.API_KEYS.index(self.API_KEY) - 1) % len(self.API_KEYS)]

        # Searching for a workable key
        while True:
            # Testing selected API key
            try:
                # If key is invalid, removed or has not `users` scopes it will raise exception
                user = cloudconvert.User.user()

                # If key is valid, checking the remaining minutes
                if user['credits'] == 0:
                    raise cloudconvert.exceptions.ClientError()

            # If key is invalid or not workable
            except cloudconvert.exceptions.ClientError:
                # If it was the last key in the list, then the key was not found
                if self.API_KEY == last_api_key:
                    sublime.error_message('No available API keys! Please create your own or switch to offline mode by editing settings')
                    return False

                # If there are still keys in the list left, go to another one
                self.API_KEY = self.API_KEYS[(self.API_KEYS.index(self.API_KEY) + 1) % len(self.API_KEYS)]
                cloudconvert.configure(api_key=self.API_KEY)
                continue

            else:
                # Key was found, break loop
                break

        def convert(engine: str, dpi: int) -> None:
            """ Online conversion process itself through the API is made into
                a separate function, so that you can start it in a new thread
                and not freeze the main thread """

            # Creating job with passed parameters
            job = cloudconvert.Job.create(payload={
                'tasks': {
                    'import-svg': {
                        'operation': 'import/upload'
                    },
                    'convert-svg-to-png': {
                        'operation': 'convert',
                        'input_format': 'svg',
                        'output_format': 'png',
                        'engine': engine,
                        'input': [
                            'import-svg'
                        ],
                        'pixel_density': dpi
                    },
                    'export-png': {
                        'operation': 'export/url',
                        'input': [
                            'convert-svg-to-png'
                        ],
                        'inline': False,
                        'archive_multiple_files': False
                    }
                }
            })

            # Getting IDs of tasks which we will still work with
            for task in job['tasks']:
                if task['operation'] == 'import/upload':
                    upload_task_id = task['id']
                elif task['operation'] == 'export/url':
                    export_task_id = task['id']

            # Getting upload task and uploading file
            upload_task = cloudconvert.Task.find(id=upload_task_id)
            cloudconvert.Task.upload(file_name=input_file_name, task=upload_task)

            # Waiting for conversion and getting URL to download result
            export_task = cloudconvert.Task.wait(id=export_task_id)
            file = export_task.get('result').get('files')[0]

            # Downloading picture
            cloudconvert.download(filename=output_file_name, url=file['url'])

        # Creating online conversion in new thread to not freeze main thread
        Thread(target=convert, args=(engine, dpi,), daemon=True).start()

        # Conversion was completed successfully
        return True

    def convert_offline(self, input_file_name: str, output_file_name: str) -> bool:
        """ Converts file from SVG to PNG by installed converters on device """

        # Getting settings for the further use
        dpi = self.settings.get('dpi')
        engine_name = self.settings.get('offline', {}).get('engine')

        # Getting command template of selected engine
        engine = self.converters.get(engine_name)

        # If selected engine not supported
        if engine_name not in self.converters.keys():
            sublime.error_message('"{}" converter not supported. Please choose converter only from suggested list!'.format(engine_name))
            return False

        # If selected engine not installed
        if not which(engine.split()[0]):
            sublime.error_message('"{}" converter not installed or not in PATH'.format(engine_name))
            return False

        # Generating full command from command template
        cmd = engine.format(name=input_file_name, out=output_file_name, dpi=dpi)

        # Execute conversion in background
        os.popen(cmd)

        # Conversion was completed successfully
        return True
