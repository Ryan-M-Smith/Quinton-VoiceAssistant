# Changing Quinton's Voice

Quinton does TTS (text-to-speech) using Espeak, and can use a variety of voices. While Espeak comes with a good amount of pre-installed voices,
you can also install Mbrola voices if you want. These instructions will help you find and use a different Espeak default voice as well as install
and use an Mbrola voice.

**NOTE:** Throughout the file you will see linux commands with brackets in them. These denote fields the the user provides content for and do
not have one particular entry that must be used.

---

## Finding a voice

To get a list of the default voices Espeak offers, open a command prompt and type `espeak --voices`.

To get a list of voices in a certain language, type: `espeak --voices={language code}`

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: `espeak --voices=en` for all English voices

Note that this will also display all of the usable Mbrola voices for that language, even if you don't have them installed.

## Setting the voice

1. Open `../data/config/config.yaml` with any text/code editor. If you are in the `Quinton-VoiceAssistant` directory, go to `data/config/config.yaml`.
2. Navigate to document 3 (the third triple hyphen [`---`])
3. Map the key `voice` to the name (full or abbreviated) of the voice you've selected
4. Save and exit

---

## Installing and Using Mbrola Voices

For this example, I will be using apt-get. Be sure to use the correct package manager/installer for your distribution.

1. Run `sudo apt-get install mbrola-{voice name}`

    &nbsp;&nbsp;&nbsp;&nbsp;Example: `sudo apt-get install mbrola-us2`

    &nbsp;&nbsp;&nbsp;&nbsp;For a complete list of voice names, see the [Espeak voices list](https://github.com/numediart/MBROLA-voices) on GitHub.

2. Test the voice in Espeak with `espeak -v mb-{voice name} "{Text to speak}"`

   &nbsp;&nbsp;&nbsp;&nbsp;Example: `espeak -v mb-us2 "Hello, World"`

3. To set it as Quinton's voice, follow the steps above
