# FILENAME: gttstest.py
# A test using the gTTS Python Library

from gtts import gTTS
tts = gTTS("Hello World.")
tts.save("hello.mp3")
