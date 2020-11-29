# Quinton-VoiceAssistant Changelog

## Unreleased (Expected v0.2.0)

* **Added**
  * The ability for the software to utilize the dictionary merge operator (`|`/`|=`) in Python 3.9
    * For those with 3.8, the old method is still included and is
      not being removed any time soon, so there's no need to upgrade.
  
  * The cache is now scanned for leftover files and they are deleted (e.g., `None.wav` when something fails)

* **Changed**
  * Refactored the gitignore
    * `__pycache__` directories are now ignored
    * Other unneeded files are also now ignored (like `/data/config/config.test.py`)
  * Clarified some comments
  <!-- * Some functionality using the `os` library now uses the `subprocess` library -->

## v0.1.1 - Released 2020-11-10

* **Added**
  * A new, shorter, easier to read README
  * The `setup.py` file now automatically tracks version number from `version.txt`

* **Changed**
  * The old README is now `README-EXT.md`

## v0.1.0 - Released 2020-11-09

* The initial release of Quinton-VoiceAssistant
