# Quinton-VoiceAssistant Changelog

This changelog follows the basic format outlined on [keepachangelog.com](https://keepachangelog.com/en/1.0.0).

## Unreleased (Expected v1.0.0-alpha)

* **Added**
  * Add support for ToolKits

## v0.2.0 - Released 2020-11-29

* **Added**
  * The cache is now scanned for leftover files and they are deleted (e.g., `None.wav` when something fails)
  * The ability for the software to utilize the dictionary merge operator (`|`/`|=`) in Python 3.9
    * For those with 3.8, the old method is still included and is
      not being removed any time soon, so there's no need to upgrade.
  * Add a reference to the changelog format I use (see above)
  * Add a download URL in the `setup.py` file

* **Changed**
  * Refactored the gitignore
    * Readability is improved
    * `__pycache__` directories are now ignored
    * Other unneeded files are also now ignored (like `/data/config/config.test.py`)
  * Some calls to `os.system` have been changed to `subprocess.Popen`
    * This migration will continue, because I feel that the software should use the newer functionality.
      Also, this may remove the need to use the `os` library in some files where `os.system` is the only
      way the module is being used.
  * Changelog entries are now organized by order of importance under their respective headings
    * For example, the most important addition to the software is at the top of the **Added** section.
  * Updated [README-EXT.md](README-EXT.md)
    * The "Developing for Quinton" section has been renamed to "Contributing"
    * A new "Future Inclusions" section has been added
    * The "Different Versions" section has now been moved to "Future Inclusions" and it is now clearly
      stated that this is a concept and not something included.
  * Updated [README.md](README.md)
    * Add a "Contributing" section that refers viewers to `README-EXT.md`
  * Some extra, unused functions that were in `cache_src/cache.py` are now in `cache_src/cache_extras.py`.
  * Clarified and rewrote some comments

## v0.1.1 - Released 2020-11-10

* **Added**
  * A new, shorter, easier to read README
  * The `setup.py` file now gets the software's version number from `version.txt` (meaning it's no longer hard-coded)

* **Changed**
  * The old README is now `README-EXT.md`

## v0.1.0 - Released 2020-11-09

* The initial release of Quinton-VoiceAssistant
