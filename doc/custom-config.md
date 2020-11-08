# Creating Custom Configuration Variables

Over the course of using Quinton, you may decide you want to add functionality - but
maybe it's not to the code itself. For example, you may want to increase the espeak
word gap. By default, Quinton's configuration file doesn't come with variables to
modify that setting, but you can add them yourself by following the setps below.

## How to Do It

1. Figure out what setting you want to modify

    &nbsp;&nbsp;&nbsp;&nbsp;For this tutorial, we'll use the word gap
    example but you can use whatever you like.

2. Navigate to the configuration file

    &nbsp;&nbsp;&nbsp;&nbsp;From this directory, navigate to [../data/config/config.yaml](../data/config/config.yaml).

3. Find the best YAML document to put your new entry

    &nbsp;&nbsp;&nbsp;&nbsp;I've put all variables pertaining to Espeak
    settings in document 3 (beginning on line 102), so you can put yours
    there. If you prefer, you could even make a new document for your custom
    configuration entries (especially if you plan to make a lot of them).

    &nbsp;&nbsp;&nbsp;&nbsp;To make a new document, make a new line after the
    last line and type `---`. Anything under this divider is cosidered the fourth
    document in the file.

4. Add the new entry

    &nbsp;&nbsp;&nbsp;&nbsp;In the document you're working in, type out the name for
    your entry's key. This should be something concise and readable. In this case, the
    easiest choice would be something like `word_gap`.

    &nbsp;&nbsp;&nbsp;&nbsp;**IMPORTANT:** Because of the way the entries are read into
    Python, the key names must abide by Python's variable naming rules. This includes not
    being able to use hyphens in key names.

    &nbsp;&nbsp;&nbsp;&nbsp;Then, add a colon after the key and then add the value. The
    word gap options takes an integer which represents a time in milliseconds (with the default
    value being 10 ms), so your value should be something alon those lines. Let's say you really
    want a fast-talking voice assistant, so you want the word gap to only be 5 ms. In this case,
    you'd set the value to 5, making your entry look like:

    ```yaml
      word_gap: 5
    ```

5. Adding a corresponding Python variable

    &nbsp;&nbsp;&nbsp;&nbsp;Now that you've added a new YAML pair, you need to give Python a place
    to store the number you put in. This is done in [config.py](../src/config_src/config.py). In the
    file, at the class' top-level, there are a bunch of empty variable declarations. There is also a
    notice about custom configuration variables. For organizational purposes, you might want to put
    your variable under the notice, but it is by no means required.

    &nbsp;&nbsp;&nbsp;&nbsp;To add a Python counterpart for your YAML pair, indent to the correct level,
    type in the **same name** that you used for your YAML key, type a colon, space, and then the word `int`.
    Your file should look something like this:

    ```python
      class Config:
        ... # Stuff before

        word_gap: int

        ... # Stuff after

    ```

6. Using the variable

  &nbsp;&nbsp;&nbsp;&nbsp;We now have a way to get the value from a YAML key-value pair to a Python variable,
  and now we have to use that variable. To do so, navigate to [voiceassistant.py](../src/voiceassistant.py) and
  find the fucntion called `speak()`. A little ways down, underneath a block comment, you should see a line that
  looks like:

  ```python
    espeak_args = f"espeak -v {self.cfg.voice} -s {str(self.cfg.speed)} -f {str(DATA_PATH)} -w {str(AUDIO_PATH)}"
  ```

  &nbsp;&nbsp;&nbsp;&nbsp;It's the first line under a `try-except` block. Here, arguments are passed to Espeak so
  the command can be run to speak the voice assistant's reply. Before the closing quotation mark, add a space and type
  `-g {str(self.cfg.word_gap)}`. This will leave the line looking like:

  ```python
    espeak_args = f"espeak -v {self.cfg.voice} -s {str(self.cfg.speed)} -f {str(DATA_PATH)} -w {str(AUDIO_PATH)} -g {str(self.cfg.word_gap)}"
  ```

## Closing

That's it! The next time you run the software, Quinton will reply with a word gap of 5 ms. This tutorial showed you how
to add a custom entry for an Espeak parameter, to add something different, such as an additional timezone, would work about
the same (it would just require a lot more modification of the Python code). All configuration variables can be accessed by
using `self.cfg.name`, so it's very easy to use the Python equivalents of the YAML keys. This way, there is an easy, readable
way to access configuration data from anywhere in the code at any time.

Note that you can only access the configuration in files that are set up with an instance of the `Config` class. A quick way to
tell if a particular file is set up is if it has this line:

```python
  from config_src.config import Config
```

I hope this tutorial was helpful to you in your quest to modify `Quinton-VoiceAssistant`.
