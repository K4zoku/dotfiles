## SVG Viewer

#### About

SVG Viewer is Sublime Text 3 plugin for viewing SVG files as pictures.<br>
It is an improved version of the original [SVG Preview](https://github.com/chunqiuyiyu/sublime-svg-preview)


#### Installation

###### Plugin

1. Make sure you already have [Package Control](https://packagecontrol.io/) installed
2. Open command pallete by pressing <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
3. Choose "**Package Control: Install Package**" and then press <kbd>Enter</kbd>
4. Select "**SVG Viewer**" and press <kbd>Enter</kbd>

###### Converter

After installing plugin, you can use it only in online mode.<br>
If you want use plugin in offline mode you should install SVG to PNG converter<br>
By default we support these converters:

- [CairoSVG](https://cairosvg.org/)
- [Inkscape](https://inkscape.org/)
- [ImageMagick](https://imagemagick.org/)
- [SVGExport](https://github.com/shakiba/svgexport/) (DPI not supported)

But you can [add](#adding-converter) another converter


#### Using

1. Open SVG file
2. Open command pallete and select "**SVG Viewer: View SVG**"
3. (if fisrt run) Choose SVG converter from the suggested converters
4. Profit!


#### Settings

If you want edit settings, key bindings or converters, do:<br>
Preferences &#8594; Package Settings &#8594; Settings / Key Bindings / Converters - Edit


#### Adding converter

If you want to use another SVG to PNG converter, do:

1. Generate command and name of your converter, such as this
```json
{
    "converter": "converter --input-file \"{name}\" --output-file \"{out}\" --dpi {dpi}"
}
```
2. Open converters.json file (Preferences &#8594; Package Settings &#8594; Converters - Edit) and add this string
3. Reopen Sublime Text, open command pallete, choose "**SVG Viewer: Change Converter**" and choose your converter
4. Profit!
