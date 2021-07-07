# Quinton-VoiceAssistant

## This is Quinton; a voice assistant, similar to Siri, Google Assistant, and Amazon Alexa, but with many differences and limitations

## Reader's Note

This is an abridged version of the project's README. For the complete README, please see [README-EXT.md](#README-EXT.md)

---

## Table of Contents

1. [Installation Prerequisites](#installation-prerequisites)
    * [Requirements](#requirements)
        * [Python Version](#python-version)
        * [PyPI Requirements (`pip` requirements)](#pypi-requirements-pip-requirements)
        * [Other Requirements](#other-requirements)
        * [API Keys](#api-keys)

2. [Installing and Running the Software](#installing-and-running-the-software)

3. [Contributing](#contributing)

4. [Software Information](#software-information)
    * [License](#license)
    * [Copyright](#copyright)
    * [Finding the Software](#finding-the-software)
    * [Reporting Bugs](#reporting-bugs)
    * [Feature Requests](#feature-requests)

5. [Resources](#resources)

---

## Installation Prerequisites

### Requirements

#### Python Version

You will need to install and run Quinton-VoiceAssistant with Python 3.8 or newer. Download and install the correct
build and version of Python for your operating system [here](https://python.org/downloads).

**macOS Users:** If you prefer, you can install Python via Homebrew rather than from source.

#### PyPI Requirements (`pip` requirements)

* `omxplayer-wrapper`
* `phonetics`
* `pyalsaaudio`
* `pyaudio`
* `pyowm`
* `pytz`
* `pyyaml`
* `speechrecognition`
* `tinytag`

#### Other Requirements

There are some packages that Quinton-VoiceAssistant requires that need to be installed from your package manager.
These dependencies are installed by running the setup script, so there is not need to install them separately unless
you choose to. A table of the required packages for Debian, Ubuntu, and Manjaro systems is provided below. If you use
a different distribution or package manager, you can search for packages for your system [here](https://pkgs.org).

| Debian/Ubuntu     | Fedora                                 | Manjaro          |
| ---------------   | ------                                 | -------          |
| `portaudio19-dev` | `portaudio-devel`; `redhat-rmp-config` | `portaudio`      |
| `python3-espeak`  | `espeak-devel`                         | `python-pyaudio` |
| `python3-pyaudio` | `python3-pyaudio`                      | -                |
| `espeak`          | `espeak`                               | `espeak`         |
| `libbz2-dev`      | `bzip2-devel`                          | `bzip2`          |
| `sox`             | `sox`                                  | `sox`            |
| `ffmpeg`          | `ffmpeg`                               | `ffmpeg`         |

**NOTE:** `omxplayer` can be used instead of `ffmpeg` on a Raspberry Pi running Raspberry Pi OS.

**NOTE:** If you try to run the software and get an error involving one of these packages, (such as a `ModuleNotFoundError`
for `_bz2`), you may need to rebuild your Python installation. See [this](https://stackoverflow.com/questions/12806122/missing-python-bz2-module)
StackOverflow thread for more information.

#### API Keys

In order for Quinton to run, you will need to have a Houndify and OpenWeatherMap accounts with valid API keys. The good news is, all of
this is free. Both services offer premium subscription options if you decide you want to upgrade your account in the future (to increase your daily API
call/credit allotment), but it's completely optional. In addition, both accounts can be signed up for without the use of a credit card.

For complete instructions on how to set up/register API keys for both services, see [README-EXT.md](#README-EXT.md)

**NOTE:** You must put all API keys in the [credentials.yaml](credentials.yaml) file for everything to work properly!

### Installing and Running the Software

Before running any commands, make sure you're in the source directory. Also, be sure to use the correct Python versions/commands
for your system. For example, your Python interpreter may be run by calling `python3.9` rather than `python3`. In these examples,
I will be using `python3`.

In certain cases, you may have to run `setup.py install` as root. If you don't want to use `sudo`, you can use the `--user` argument:

```bash
sudo setup.py install <args>
# --- OR --- #
setup.py install <args> --user # Will install in the current user's site-package directory
```

With the modified build behavior, one command can be used to install all dependencies as well as the software for Linux and macOS.
As of now the supported package managers are:

* Homebrew (`brew`)
* `apt-get`
* `yum`
* `dnf`
* `pacman`

**If your system meets these requirements, you can install by running:**

```bash
# NOTE: `True` must be capitalized for the command(s) to work properly.
python3 setup.py install --pkg-install=True
# --- OR --- #
python3 setup.py install -k True # An alternative to the above command
```

If your system doesn't meet these requirements or you want to install the dependencies separately, see
[README-EXT.md](README-EXT.md#manual-dependency-installation).

**Once everything is installed, type** `voiceassistant` **in your terminal to run the program.**

## Contributing

To learn more about how to contribute, see ["Contributing"](README-EXT.md#contributing) in README-EXT.md.

## Software Information

### License

Quinton-VoiceAssistant is licensed under the GNU General Public License v3+. For more information, see [LICENSE.txt](LICENSE.txt).

### Copyright

Quinton-VoiceAssistant is Copyright (c) 2020-2021 by Ryan Smith

### Finding the Software

Quinton-VoiceAssistant is free and open-source software. You can find the code on
[GitHub](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant).

### Reporting Bugs

To report any bugs, contact me by email at <rysmith2113@gmail.com> or raise an
[issue on Github](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues).

### Feature Requests

Feature requests for Quinton-VoiceAssistant are welcome! You can send them in by email or
raise an issue on the repo. When you do, choose the feature request issue template and follow
the directions to fill everything out.

## Resources

* [Python Downloads Page](https://python.org/downloads)
* [Homebrew Installation Instructions](https://brew.sh)
* [Linux/Unix Package Search](https://pkgs.org)
* [My GitHub](https://www.github.com/Ryan-M-Smith)
* [The Quinton-VoiceAssistant Repository](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant)
* [Issues Page](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues)
