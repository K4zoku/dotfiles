# SyntaxFold - Sublime Text Plugin

A plugin for [Sublime Text][st] 3 that folds/collapses or unfolds/expands code blocks based on specific syntax defined by the User rather than indent.

<i>Note: This plugin does not create folding markers (the functionality for creating these markers is not exposed within the Sublime Text API). The folding functionality provided by this plugin relies on using keyboard shortcuts assigned by the User or by invoking fold commands through the command panel.</i>

## Background
This plugin was created for any language that uses named regions similar to languages like VB, C++ and C# (see [here][vs]). Where possible, use a plugin created specifically for your syntax.

Expanding and collapsing areas is also supported in non-source files, such as text files (Sublime Text regards HTML as belonging to a `text` scope name).

## Installation
* Use [Sublime Package Control](http://wbond.net/sublime_packages/package_control "Sublime Package Control")
* <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> then select `Package Control: Install Package`
* Type `SyntaxFold` and press <kbd>ENTER</kbd>

Alternatively Clone this repository to your Sublime Text packages directory.

### Setup
The settings file can be accessed through `Preferences -> Package Settings -> Settings - User`.  It will be initially populated with the following settings.

```json
{
    "config":[
        {
            "scope": "source.java, source.js, embedding.php",
            "startMarker": "//region",
            "endMarker":"//endregion"
        },
        {
            "scope": "source.cs",
            "startMarker":"#region",
            "endMarker":"#endregion"
        },
        {
            "scope": "source.c++, source.c",
            "startMarker":"#pragma region",
            "endMarker":"#pragma endregion"
        },
        {
            "scope": "text.html.basic",
            "startMarker":"<!--region-->",
            "endMarker":"<!--endregion-->"
        },
        {
            "scope": "text.plain",
            "startMarker":"---region---",
            "endMarker":"---endregion---"
        }
    ]
}
```

Add or remove fold region objects to meet your needs.  Note the `scope` key. Utilize this key to filter which source file types for which the start and end markers are active. To determine the scope name for a file type use `Tools -> Developer -> Show Scope Name` or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>.

The `scope` key may contain a comma separated list of scopes for which the markers should be active. The settings file above supports, for example, Java, Javascript and PHP files folding through the same `//region` and `//endregion` markers since the defined scope is `"source.java, source.js, embedding.php"`.


## Usage
Use the [keybindings](#command-examples) to fold/unfold your code

### Key Bindings ###

The following is an excerpt of the default key bindings:

```js
[
//Fold all code blocks
  { "keys": ["alt+0", "alt+0"],
    "command": "fold_all" },

// Unfold all code blocks
  { "keys": ["alt+shift+0", "alt+shift+0"],
    "command": "unfold_all"},

// Toggle fold current code block
  { "keys": ["alt+1", "alt+1"],
    "command": "toggle_fold_current"},
]
```

### Command Reference

A list of commands have been added to the command palette and can be accessed using <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>.
All commands start with "SyntaxFold : [command name]".

***Fold All***:
Fold/collapse all syntax delimited blocks in the current document.

***Unfold all***:
Unfold/expand all syntax delimited blocks in the current document.

***Toggle Fold Current***:
Folds/collapses or Unfolds/expands the syntax delimited block where the cursor is placed on.

***Open README***:
Open this readme file.

### Saving fold state

This package doesn't support saving the folded state of a file (remembering which blocks you have folded) but there is a package called BufferScroll perfectly suited to that https://packagecontrol.io/packages/BufferScroll


<!-- Links -->
[vs]:http://blogs.msdn.com/b/zainnab/archive/2013/07/12/visual-studio-2013-organize-your-code-with-named-regions.aspx
[st]: http://sublimetext.com/
