# FILENAME: pyttsxtest.py
# DESCRIPTION: A test using the pyttsx Python library

import pyttsx3

engine = pyttsx3.init(driverName="espeak")

voices = engine.getProperty("voices")

for voice in list(voices):
	if "english" in str(voice):
		print(voice.id)

engine.setProperty("voice", "english-us")
engine.setProperty("volume", 0.5)
engine.setProperty("rate", 150)

engine.say("Hello world")
engine.runAndWait()