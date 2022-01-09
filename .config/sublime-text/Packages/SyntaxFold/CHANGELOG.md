SublimeText Changelog
====================

v1.1.0 (2014-10-30)
-------------------

- Added support for folding based on startMarker only, the code will fold to the next startMarker or to the end of the document if there is none


v1.1.1 (2014-04-16)
-------------------

- fixed bug in setting package path for linux and mac (credit: mfkddcwy)


v2.0.0 (2017-01-02)
-------------------

- Active fold start and end markers are now selected by source syntax of the current file. These changes break compatability with the settings file of the previous versions. The user settings file must be updated. See default settings or README.md for details.


v2.1.0 (2017-04-18)
-------------------

- Added folding support to files containing `text` in their scope name, allowing HTML files to be folded (`text.html.basic` scope).


v2.2.0 (2017-05-01)
-------------------

- Modified the current region folding commands (fold and unfold) in order to toggle-fold in a single command. Edited the settings in order to use the same markers for folding in other languages (reduced the example in README.md).

v2.3.0 (2019-12-18)
-------------------
- fixed issue 40 (https://github.com/jamalsenouci/sublimetext-syntaxfold/issues/40)

v2.4.0 (2019-06-07)
-------------------
- fixed issue #43 (https://github.com/jamalsenouci/sublimetext-syntaxfold/issues/43) 
- commands have been prefixed with syntaxfold_
