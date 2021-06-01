# Quinton-VoiceAssistant

## This is Quinton; a voice assistant, similar to Siri, Google Assistant, and Amazon Alexa, but with many differences and limitations

---

## Table of Contents

1. [Basic Information](#basic-information)
    * [About the Name](#about-the-name)
    * [Features and Limitations](#features-and-limitations)
        * [Features](#features)
        * [Limitations](#limitations)
    * [Recognizable Commands](#recognizable-commands)

2. [How Quinton Works](#how-quinton-works)

3. [Installation Prerequisites](#installation-prerequisites)
    * [Requirements](#requirements)
        * [Python Version](#python-version)
        * [PyPI Requirements (`pip` requirements)](#pypi-requirements-pip-requirements)
        * [Other Requirements](#other-requirements)
        * [API Keys](#api-keys)
    * [Houndify Sign-up Instructions](#houndify-sign-up-instructions)
        * [How to Sign Up for a Houndify account](#how-to-sign-up-for-a-houndify-account)
        * [How to Register a Client ID and Key](#how-to-register-a-client-id-and-key)
        * [How to Test Out the Houndify API Online](#how-to-test-out-the-houndify-api-online)
        * [Houndify Credit Usage Info and Account Upgrading](#houndify-credit-usage-info-and-account-upgrading)
    * [OpenWeatherMap Sign-up Instructions](#openweathermap-sign-up-instructions)
        * [How to Sign Up for an OpenWeatherMap account](#how-to-sign-up-for-an-openweathermap-account)
        * [Finding Your Default API Key](#finding-your-default-api-key)
        * [Registering a New API Key](#registering-a-new-api-key)
        * [Changing the Name of a Key](#changing-the-name-of-a-key)
        * [How to Test Out the OpenWeatherMap API Online](#how-to-test-out-the-openweathermap-api-online)
        * [OpenWeatherMap Usage Info and Account Upgrading](#openweathermap-usage-info-and-account-upgrading)

4. [Actually installing the software](#actually-installing-the-software)
    * [Manual Dependency Installation](#manual-dependency-installation)
      * [With the Build Functionality](#with-the-build-functionality)
      * [Without the Build Functionality](#without-the-build-functionality)

5. [Future Inclusions](#future-inclusions)
    * [Different Versions](#different-versions)
    * [ToolKits](#toolkits)
    * [More Build Support](#more-build-support)

6. [Miscellaneous](#miscellaneous)
    * [Using the `pyowm.caching` Module](#using-the-pyowm.caching-module)

7. [Contributing](#contributing)
    * [Code Modifications](#code-modifications)
    * [Creating ToolKits](#creating-toolkits)

8. [Software Information](#software-information)
    * [License](#license)
    * [Copyright](#copyright)
    * [Finding the Software](#finding-the-software)
    * [Reporting Bugs](#reporting-bugs)

9. [Resources](#resources)

---

## Basic Information

### About the Name

As you've probably already figured out, the voice assistant's name is Quinton. If you don't like the name and want to change it, just
modify the wake word in [config.yaml](data/config/config.yaml).

### Features and Limitations

#### Features

* Listen to commands
* Reply to commands
* Record command data (history, audio responses)
* Recall previously used commands from a cache
* Log error data
* Is highly customizable

#### Limitations

* Small dictionary - can only recognize 47 words
* Task count - can only perform 9 tasks, 2 of which currently don't work
* Not the fastest - replies can take from 6-9 seconds to be spoken
* Not the most elegant to set up
  * No companion app (yet)
  * Doesn't have the most intuitive setup wizard

### Recognizable Commands

#### As of now, Quinton can recognize and reply to the following commands

* Asking the time
  * ex. "What time is it?"; "Tell me the time"

* Getting the date
  * ex. "What is the date?"; "Tell me the date"

* Getting the weather
  * ex. "What is the weather like?"; "Tell me the weather"

* Recording information (such as your favorite animal)
  * ex. "My favorite animal is a/an `animal name`"

* **Future Inclusion:** Smart home control
  * "Turn on/off the light"

    _NOTE: As of now, these kinds of commands are recognized, but they give an "operation not permitted" message_

## How Quinton Works

All of Quinton's text to speech is done by the Houndify API, but everything is called via [Uberi's](https://www.github.com/Uberi)
[SpeechRecognition library](https://www.github.com/Uberi/speech_recognition). A Houndify home automation client is used to receive the
commands. After the speech is converted to text, it is processed and replied to locally (as opposed to having a reply transmitted
from the internet).

## Installation Prerequisites

### Requirements

#### Python Version

You will need to install and run Quinton-VoiceAssistant with Python 3.8 or newer. Download and install the correct
build and version of Python for your operating system [here](https://python.org/downloads).

**macOS Users:** If you'd prefer, you can install Python via Homebrew rather than from source.

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

There are some non-PyPI packages that Quinton-VoiceAssistant requires that need to be installed from your package manager.
These dependencies are installed by running the setup script, so there is not need to install them separately unless
you choose to. A table of the required packages for Debian, Ubuntu, Fedora, and Manjaro systems is provided below. If you use
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

In order for Quinton to run with 100% functionality, you will need to have a Houndify and OpenWeatherMap accounts with valid API keys.
The good news is, all of this is free. Both services offer premium subscription options if you decide you want to upgrade your account
in the future (to increase your daily API call/credit allotment), but it's completely optional. In addition, both accounts can be signed up
for without the use of a credit card.

**NOTE:** You only need both accounts for _100%_ functionality. If you don't plan to use the weather features, you can use the software with
only Houndify keys.

**NOTE:** You must put all API keys in the [credentials.yaml](credentials.yaml) file for everything to work properly!

---

Continue reading for sign-up/setup instructions. If you want to wait until later to sign up, click [here](#actually-installing-the-software)
to skip to the software installation instructions (i.e., the section after the next one).

---

### Houndify Sign-up Instructions

#### How to Sign Up for a Houndify account

1. Navigate to [houndify.com](https://www.houndify.com)
2. Click on the blue button labeled "Try it Free" in the upper right
3. Make sure you're selected on "Create a developer account"
4. Fill out all of the required fields and agree to the terms of service
5. Click "Get Started"

#### How to Register a Client ID and Key

1. On the dashboard, under "My Clients", select "New Client"
2. Enter a name for the client (any name; it doesn't matter)
3. For the platform, select "Home Automation"
4. In the Enabled Domains section, start typing "speech to text only", and select it when it appears. Don't select any other domains.
5. Click "Save & Continue"
6. Your client ID and key should appear as well as some statistics about your Houndify speech-to-text activity.

For more information about how you use your Houndify client, click on "View Analytics page" to see information about how you use
credits, how often you utilize speech-to-text, domain usage information, and query usage.

**NOTE:** the section labeled "Domain Distribution" will most likely only display "Speech To Text Only" as 100% of the distribution unless
you make a text query (e.g., typing in a command on the website's API tester).

#### How to Test Out the Houndify API Online

1. If you aren't already on the "Overview & API Keys" page, click on "Dashboard" at the top of the page. Otherwise, skip to step 3.
2. Select your client
3. On the left-hand side of the page, select "Try the Houndify API"
4. Type or speak a command. If you're speaking, make sure you allow microphone acccess
5. Because the "Speech To Text Only" domain is enabled, the only response you'll get is what you typed/spoke spoken back to you,
   but this is expected.

If you want to play around with some other domains to get actual responses, just create another client. As far as I know, there is no
limit to how many clients you can have.

#### Houndify Credit Usage Info and Account Upgrading

For free users, Houndify imposes a limit of 100 credits per day per client, with a limit of 10 queries per second.
You can gain more credits by upgrading your account. To do this, select the "Pricing" tab at the top of the page to view
the prices for each tier and to see what is included in each. Note that you must verify your account before you are
allowed to upgrade, and all tiers except Enterprise limit you to 10 queries per second.

For more information on how credits are used and how credit usage is calculated, scroll down a little bit on the Pricing page or
just click [here](https://www.houndify.com/pricing#how-do-credits-work).

### OpenWeatherMap Sign-up Instructions

#### How to Sign Up for an OpenWeatherMap account

1. Navigate to [openweathermap.org](https://openweathermap.org)
2. Click on "Sign in" in the upper right
3. Click on "Create an Account"
4. Fill out all fields, verify your age, agree to the terms and conditions, customize your mail preferences, and complete the
   reCAPTCHA.
5. Click "Create Account"

#### Finding Your Default API Key

All OpenWeatherMap accounts come with a default API key named "Default" (but the name can be changed, see [below](#changing-the-name-of-a-key)).

To find your default API Key:

1. On the lower navigation bar (under the one with the search bar) click on "API Keys". If this step is causing you some trouble (it was confusing
   for me at first), the link is [here](https://home.openweathermap.org/api_keys). Note that this link only works if you're signed in.
2. A default key should be pre-generated for you.

#### Registering a New API Key

According to OpenWeatherMap:

> You can generate as many API keys as needed for your subscription. We accumulate the total load from all of them.

So to do it:

1. Make sure you're on the "API Keys" tab (step 1 above)
2. Under "Create Key", type in a name for your key
3. Click "Generate"

#### Changing the Name of a Key

Note that for any API key (even the default one), you can change its name by clicking on the little pencil and paper icon to the right
of the current name. If you have multiple keys, you can delete any of them by clicking the "x" next to the change-name icon. Press "OK"
if a box pops up asking to verify the key deletion (I know this happens in Chrome).

#### How to Test Out the OpenWeatherMap API Online

To test the OpenWeatherMap API, just type the name of your city, county, or country in the search bar at the top. When you select your
correct result, you should see the weather data in your area that you are allowed to see with your account. Note that clicking on your result
may redirect you the first time you try to search, and your data won't show up. If this happens, search again in the white search bar that appears
a bit further down on the page (not the gray one at the top you searched in before). In order from left to right, the buttons to the right of the search
bar are: a pointer button to see weather for your predicted location, a button labeled "Different Weather?" to report incorrect weather forecasts and
submit a correct one, and buttons to switch between Fahrenheit and Celsius. Note that the location prediction might get your location wrong. Also, from
my experience, OpenWeatherMap has been very accurate, so I don't think you would need to use the "Different Weather?" feature often if at all.

#### OpenWeatherMap Usage Info and Account Upgrading

For OpenWeatherMap, there isn't a credit system or any kind of longer-term usage cap. The only restriction is that you can only make 60
calls per minute. This is probably more than any one person would need, but upgrading does allow you to get forecasts further ahead (for example,
a 16-day daily forecast reading). You can also sign up for specialized APIs that give you data like weather forecasts from up to 40 years ago.

## Actually installing the software

Before running any commands, make sure you're in the source directory. Also, be sure to use the correct Python versions/commands
for your system. For example, your Python 3.9 interpreter may be run by calling `python3` rather than `python3.9`. In these examples,
I will be using the command `python3.9`.

In certain cases, you may have to run `setup.py install` as root. If you don't want to use `sudo`, you can use the `--user` argument:

```bash
sudo setup.py install
# --- OR --- #
setup.py install --user # Will install in the current user's site-package directory
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
python3.9 setup.py install --pkg-install=True
# --- OR --- #
python3.9 setup.py install -k True # An alternative to the above command
```

**If your system meets these requirements, you can install by running:**

```bash
# NOTE: `True` must be capitalized for the command(s) to work properly.
python3.9 setup.py install --pkg-install=True

python3.9 setup.py install -k True # An alternative to the above command
```

If your system doesn't meet these requirements or you want to install the dependencies separately, see
[README-EXT.md](README-EXT.md#manual-dependency-installation).

### Manual dependency installation

If you can't install using the new command(s) because of your Linux distribution, or you'd just prefer to install the
non-Python dependencies youself, you will need a few more steps. Note that the follwing steps will work on both Linux
and macOS.

#### With the Build Functionality

If you are on macOS or a supported Linux distribution, you can opt to install non-Python dependencies separately from
the rest of the software. This can be done with the following:

```bash
python3.9 setup.py pkg_install  # Install non-Python dependencies
python3.9 setup.py orig_install # Install everything else (default `setup.py install` behavior)
```

#### Without the Build Functionality

If your Linux distribution is not supported, you will first have to install all non-Python dependencies using your
package manager. To find the correct packages for your system, see [pkgs.org](https://pkgs.org). Then, install as
usual.

```bash
# An example for RPM users
sudo rpm -i ... # Packages
```

After that, run the following to install everything else:

```bash
python3.9 setup.py orig_install
```

## Future Inclusions

### Windows Support

At some point, I would love to have official Windows binaries of Quinton-VoiceAssistant so anyone on Windows could use the
software. This way, no one will have to poke around with installing it in Linux on Windows.

### Different versions

In the future, my hope is that there would be a few different versions of Quinton-VoiceAssistant. The one you have downloaded right now
would be the regular version, which would be used like a normal voice assistant. In addition, there would be a CLI version (Quinton-CLI)
which would work without a microphone or an audio output device (speakers, headphones, etc.), and a dedicated developer version (Quinton-VA-Dev)
which would contain templates for developing Quinton ToolKits.

These alternate versions are still waiting to be worked on and don't have set release dates. As of now, Quinton-CLI is very likely to be
eventually released, and Quinton-VA-Dev is still largely conceptual due to the fact that I am currently integrating ToolKits _and_ their
development templates into Quinton-VoiceAssistant (not partially into Quinton-VoiceAssistant and partially into Quinton-VA-Dev).

### ToolKits

In future versions of Quinton, there will be support for Quinton ToolKits - special Python classes designed to
add functionality to Quinton without modifying its source code directly. Instead, a Python module is put in a
directory and data from the class in the module is read by Quinton and incorporated into the software. This type
of functionality would be used to expand Quinton's skill set, such as allowing it to answer math questions or get
your current location; stuff that isn't built in by default. This approach allows Quinton to be nearly infinitely
expandable.

When the feature is released, official documentation will be written here. If you are interested in the idea of
Quinton ToolKits and want to read about the current working ideas for the feature, please see [doc/toolkits.md](doc/toolkits.md).

My hope is that this feature will be available by Quinton-VoiceAssistant release 1.0.0, and software betas including
experimental versions of the functionality will be released prior to that.

### More build support

In the future, I would like to support more package managers so that everyone can have a single-command installation experience
with Quinton-VoiceAssistant, no matter what operating system they use.

## Miscellaneous

### Using the `pyowm.caching` Module

As of v0.2.3, the `pyowm.caching` module is no longer used in the code because the feature has been depricated
in PyOWM v3.0.0. However, if you still wish to use the feature, you can do so using either of following methods:

1. Clone the whole repository

   Here, you'll be cloning the entire repository but immediately doing a `checkout` to branch `old-pyowm-caches` and
   building the software from there. This is done with the following

   <!-- A 3-space indent satifies my markdown linter, so... -->
   ```bash
   git clone https://github.com/Ryan-M/Smith.Quinton-VoiceAssistant.git
   git checkout old-pyowm-caches
   python3.8 setup.py install # Build/install Quinton-VoiceAssistant
   ```

2. Clone only the `old-pyowm-caches` branch

   If you'd prefer, you can instead clone the repository but _only_ the branch you want. This can be done with
   the following:

   ```bash
   # --branch is the long form of the -b argument
   git clone --branch old-pyowm-caches https://github.com/Ryan-M/Smith.Quinton-VoiceAssistant.git
   python3.8 setup.py install
   ```

   Notes:
      1. The above clone will still track other remote braches, such as master. If you truly _only_
         want the `old-pyowm-caches` branch, use the `--single-branch` flag as well.
      2. This branch is not under active development, and will not have the software's latest features,
         especially since bringing in changes from master would override the legacy functionality.

## Contributing

### Code Modifications

Feel free to modify Quinton-VoiceAssistant. Just abide by the rules in the [license](#license).

### Creating ToolKits

Once the ToolKit feature is released, users will (hopefully) be able to build their own ToolKits to expand Quinton's
capabilities. This will be another way users/outsiders can contribute to the project.

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

## Resources

* [Uberi's Github](https://www.github.com/Uberi)
* [Uberi's SpeechRecognition Library](https://www.github.com/Uberi/speech_recognition)
* [Houndify](https://www.houndify.com)
  * [How Houndify Credits Work](https://www.houndify.com/pricing#how-do-credits-work)
* [OpenWeatherMap](https://www.openweathermap.org)
  * [OpenWeatherMap API Keys](https://home.openweathermap.org/api_keys)
* [Python Downloads Page](https://python.org/downloads)
* [Homebrew Installation Instructions](https://brew.sh)
* [Linux/Unix Package Search](https://pkgs.org)
* [My GitHub](https://www.github.com/Ryan-M-Smith)
* [The Quinton-VoiceAssistant Repository](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant)
* [Issues Page](https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/issues)
