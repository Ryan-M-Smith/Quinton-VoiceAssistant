# Quinton-VoiceAssistant Changelog

This changelog follows the basic format outlined on [keepachangelog.com](https://keepachangelog.com/en/1.0.0).

To learn more about the specifics of my changelog structure, see [doc/changelog-struct.md](doc/changelog-struct)

## Unreleased (Expected v1.0.0-alpha)

* **Added**
  * Add support for ToolKits

## v0.3.7 - Released 2021-05-16

* **Changed**
  * The GitHub Actions workflow for this repository doesn't run as often anymore
  * Updated the documentation
    * Notably, the README files now include the Manjaro dependencies in the
      table
  * Rewrote and clarified a few things in the changelog

* **Fixed**
  * Fixed a bug where the function that clears the cache wasn't being called

## v0.3.6 - Released 2021-04-01

* **Added**
  * Added a new file (`doc/changelog-struct.md`) describing the changelog structure

* **Changed**
  * Reword some things in the changelog
  * Minor documentation updates

* **Fixed**
  * Fixed a bug where the program would crash when trying to play audio with `omxplayer`
    on Raspberry Pi
  * Fixed a bug where an undefined variable was being accessed
  * A return value of `None` from `VoiceAssistant.listen()` is now correctly handled

* **Removed**
  * Removed all audio playback code deprecated in v0.3.1

## v0.3.5 - Released 2021-03-08

* **Changed**
  * Reworded a few things in the README

* **Fixed**
  * Fixed some syntax errors causing the program to crash
  * _Finally_ the editorconfig correctly displays files with their defined indentation
    type and in the correct size. I had to dig through the EditorConfig documentation to
    find the solution, but I feel like it will be nicer to view files with a 4-tab-size
    indent than with an 8.

## v0.3.4 - Released 2021-01-29

* **Added**
  * Integrated a GitHub Actions workflow to manage code security

* **Changed**
  * Marked a previous changelog entry as a change rather than as a bugfix
  * Reworded some comments and docstrings

* **Fixed**
  * ~~The editorconfig now correctly displays files with their defined indentation
    type and in the correct size~~
    * _NOTE: This bugfix didn't work. The bug was fixed in v0.3.5._

## v0.3.3 - Released 2021-01-22

* **Added**
  * Added dependency installation support for Pacman
  * Added issue templates for bug reports and feature requests

* **Changed**
  * Update the README files to include Pacman in the list of supported package managers
  * The editorconfig file now works on shell scripts, the gitignore, and the editorconfig itself

## v0.3.2 - Released 2021-01-10

* **Added**
  * Added a `.editorconfig` file

* **Changed**
  * Updated the copyright section on all file boilerplates and README files with the year 2021
    * On that note, happy (belated) New Year! :tada:
  * The `setup.py` file has a new boilerplate that matches all the other Python files in the project
  * Reworded a few things in the changelog

## v0.3.1 - Released 2021-01-01

* **Added**
  * The README files and package lists now show `ffmpeg` as a required package to run the software

* **Changed**
  * `ffmpeg` is now the primary audio player for the software
    * `omxplayer` is still being used, but only if it's installed and only on Raspberry Pi OS
  * The `VoiceAssistant` class no longer handles audio output; only audio file creation
    * Audio output is all done by the functionality in `audioplayer.py`
  * Reworded a few things in the changelog
  * macOS is now stylized correctly in both the README files and the changelog

* **Fixed**
  * Fixed a bug causing the command subject to not be set in certain cases
  * Fixed a bug causing audio playback not to work ([#30](https://github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues/30))
  * Fixed a bug causing the setup wizard to crash

* **Deprecated**
  * All individual audio output functionality has been removed; it's all universal from `audioplayer.py`

## v0.3.0 - Released 2020-12-29

* **Added**
  * The `wizard.py` file now has a module docstring
  * Package manager dependency files for building the software

* **Changed**
  * The software is now built entirely using the `setup.py` file
    * On macOS, Debian/Ubuntu, and Fedora, you no longer have to install non-Python dependencies separately (unless you want to).
    * Users who cannot take advantage of this can build the software using the directions in
      [README-EXT.md](README-EXT.md#manual-dependency-installation).
    * Users who'd prefer to not use this new build functionality can also follow the link above for more information.
  * Updated the README files
    * Added a notice about a possible dependency error that can occur at runtime, and how to solve it.
    * Added a link to the "Other Requirements" section in the table of contents
    * Installation example commands now use Python 3.9, and the latest Python version section has been updated
  * Updated MANIFEST.in to include package dependency lists
  * Reworded some comments and docstrings

* **Fixed**
  * Fixed a broken link in the README-EXT's table of contents

## v0.2.3 - Released 2020-12-16

* **Changed**
  * Updated [README-EXT.md](README-EXT.md) with information about the PyOWM bug
    * There is a tutorial under the "Miscellaneous" section which will help you out if
      you're looking to continue to use the cache feature.
  * Made a changelog entry more readable

* **Fixed**
  * Fixed an import error involving an update to the PyOWM caching module, `pyowm.caches`

* **Removed**
  * Usage of the `pyowm.caches` module, which is depricated in PyOWM v3.0.0 ([#21](https://github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues/21))
    * If you still want to utilize the cache feature, you can clone the repository's
      [old-pyowm-cache](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/tree/old-pyowm-cache)
      branch and run the code from there. Note that on this branch, the `pyowm` module will
      run on v2.10, the newest version of the software that still supports the `pyowm.caches`
      module.

## v0.2.2 - Released 2020-12-16

* **Changed**
  * Some variables are now instantiated right before their use rather than at the top of a
    function
  * The license has my name on it now (but this probably never mattered to begin with)

* **Fixed**
  * An import bug causing the software to crash is now fixed

## v0.2.1 - Released 2020-12-13

* **Changed**
  * Usable replies are now found using dictionary lookup instead of an `if`-`elif` block
  * `cache_extras.py` now uses `pathlib` for file paths instead of paths in strings
  * `subprocess.call` is now used ubiquitously over `subprocess.Popen`
    * In addition, the remaining calls to `os.system` have been replaced with `subprocess.call`
  * The YAML configuration files now have whitespace and are more readable
  * Removed some horizontal lines (`---`) from the README files so they'll look nicer when rendered
  * Clarified some changelog entries
  * Proofread and enchanced some documentation

* **Fixed**
  * Permissions now work correctly
    * When you disable something (like audio recording), it is actually diabled
  * All data storage files are now empty
    * Some of them previously contained data from testing; this would not break the software,
      but I thought it would be nice to clear them out.

## v0.2.0 - Released 2020-11-29

* **Added**
  * The cache is now scanned for leftover files and they are deleted (e.g., `None.wav` when something fails)
  * The ability for the software to utilize the dictionary merge operators (`|`/`|=`) if you run the software with Python 3.9+
    * For those with 3.8, the old dictionary combination method is still being used in the
      code and is not being removed any time soon, so there's no need to upgrade.
  * Added a reference to the changelog format I use [(see above)](#quinton-voiceassistant-changelog)
  * Added a download URL in the `setup.py` file

* **Changed**
  * Refactored the gitignore
    * Readability is improved
    * `__pycache__` directories are now ignored
    * Other unneeded files are also now ignored (like `/data/config/config.test.py`)
  * Some calls to `os.system` have been changed to either `subprocess.Popen` or `subprocess.call`
    * This migration will continue, because I feel that the software should use the newer functionality.
      Also, this may remove the need to use the `os` library in some files where `os.system` is the only
      way the module is being used.
  * Changelog entries are now organized by order of importance under their respective headings
    * For example, the most important addition to the software is at the top of the **Added** section.
  * Updated [README-EXT.md](README-EXT.md)
    * The "Developing for Quinton" section has been renamed to "Contributing"
    * A new "Future Inclusions" section has been added
    * The "Different Versions" section has now been moved to "Future Inclusions" and it is now clearly
      stated that this is a concept and not a current part of the software.
  * Updated [README.md](README.md)
    * Added a "Contributing" section that refers viewers to `README-EXT.md`
  * Some extra, unused functions that were in `cache_src/cache.py` are now in `cache_src/cache_extras.py`.
  * Clarified and rewrote some comments

## v0.1.1 - Released 2020-11-10

* **Added**
  * Added a new, shorter, easier to read README
  * The `setup.py` file now gets version info number from `version.txt` (meaning it's no longer hardcoded)

* **Changed**
  * The old README is now `README-EXT.md`

## v0.1.0 - Released 2020-11-09

* The initial release of Quinton-VoiceAssistant
