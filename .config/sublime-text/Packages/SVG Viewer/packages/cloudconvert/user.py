from cloudconvert.resource import Resource
from cloudconvert.cloudconvertrestclient import default_client
from cloudconvert import util

class User(Resource):
    path = "v2/users"

    @classmethod
    def user(cls):
        """Locate resource e.g. current user
        Usage::
            >>> user = User.user()
        """
        api_client = default_client()

        url = util.join_url(cls.path, "me")
        res = api_client.get(url)
        try:
            return res["data"]
        except:
            return res
