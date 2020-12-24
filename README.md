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

2. [Installing the software](#actually-installing-the-software)
    * [On Linux](#on-linux)
    * [On MacOS](#on-macos)

3. [Contributing](#contributing)

4. [Software Information](#software-information)
    * [License](#license)
    * [Copyright](#copyright)
    * [Finding the Software](#finding-the-software)
    * [Reporting Bugs](#reporting-bugs)

5. [Resources](#resources)

---

## Installation Prerequisites

### Requirements

#### Python Version

You will need to install and run Quinton-VoiceAssistant with Python 3.8 or newer. Download and install the correct
build and version of Python for your operating system [here](https://python.org/downloads). As of this version's,
release date, the latest version of Python is 3.9.1.

**MacOS Users:** If you prefer, you can install Python via Homebrew rather than from source.

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
you choose to. A table of the required packages for Debian, Ubuntu, and Fedora systems is provided below. If you use
a different distribution or package manager, you can search for packages for your system [here](https://pkgs.org).

| Debian/Ubuntu     | Fedora                                 |
| ---------------   | ------                                 |
| `portaudio19-dev` | `portaudio-devel`; `redhat-rmp-config` |
| `python3-espeak`  | `espeak-devel`                         |
| `python3-pyaudio` | `python3-pyaudio`                      |
| `espeak`          | `espeak`                               |
| `libbz2-dev`      | `bzip2-devel`                          |
| `sox`             | `sox`                                  |

**NOTE:** If you try to run the software and get an error involving one of these packages, (such as a `ModuleNotFoundError`
for `_bz2`), you may need to rebuild your Python installation. See [this](https://stackoverflow.com/questions/12806122/missing-python-bz2-module)
StackOverflow thread for more information.

#### API Keys

In order for Quinton to run, you will need to have a Houndify and OpenWeatherMap accounts with valid API keys. The good news is, all of
this is free. Both services offer premium subscription options if you decide you want to upgrade your account in the future (to increase your daily API
call/credit allotment), but it's completely optional. In addition, both accounts can be signed up for without the use of a credit card.

For complete instructions on how to set up/register API keys for both services, see [README-EXT.md](#README-EXT.md)

**NOTE:** You must put all API keys in the [credentials.yaml](credentials.yaml) file for everything to work properly!

### Installing the software

Before running any commands, make sure you're in the source directory. Also, be sure to use the correct Python versions/commands
for your system. For example, your Python 3.9 interpreter may be run by calling `python3` rather than `python3.9`. In these examples,
I will be using `python3.9`.

To install the software, you can just run `python3.9 setup.py install`.

#### On Linux

Debian/Ubuntu Systems

```bash
sudo apt-get install python3-espeak python3-pyaudio espeak libbz2-dev

python3.8 setup.py install
```

Fedora Systems

```bash
# This will work the same for DNF
sudo yum install portaudio-devel redhat-rmp-config espeak bzip2-devel pyaudio

python3.8 setup.py install
```

#### On MacOS

To install, make sure you have Homebrew. For installation instructions, go to [brew.sh](https://brew.sh).

```bash
brew install python3-espeak python3-pyaudio espeak libbz2-dev

python3.8 setup.py install
```

## Contributing

To learn more about how to contribute, see ["Contributing" in README-EXT.md](README-EXT.md#contributing)

## Software Information

### License

Quinton-VoiceAssistant is licensed under the GNU General Public License v3+. For more information, see [LICENSE.txt](LICENSE.txt).

### Copyright

Quinton-VoiceAssistant is Copyright (c) 2020 by Ryan Smith

### Finding the Software

Quinton-VoiceAssistant is free and open-source software. You can find the code on
[GitHub](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant).

### Reporting Bugs

To report any bugs, contact me by email at <rysmith2113@gmail.com> or raise an
[issue on Github](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues).

## Resources

* [Python Downloads Page](https://python.org/downloads)
* [Homebrew Installation Instructions](https://brew.sh)
* [Linux/Unix Package Search](https://pkgs.org)
* [My GitHub](https://www.github.com/Ryan-M-Smith)
* [The Quinton-VoiceAssistant Repository](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant)
* [Issues Page](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues)
