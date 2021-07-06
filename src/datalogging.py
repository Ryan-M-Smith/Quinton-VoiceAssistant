
#
# FILENAME: logging.py | Quinton-VoiceAssistant
# DESCRIPTION: Data logging functionality
# CREATED: 2020-09-05 @ 6:04 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

"""
	Includes data logging functionality which allows Quinton to:
		* Speak error output to the user
		* Log error data to a log file in `../data/logs`

	The speech functionality is very similar to the `VoiceAssistant.speak()`
	function, but they have a few differences. Because the `VoiceAssistant` class
	may not always be able to use its `speak()` function (e.g., like when no
	configuration is loaded), this separate function will allow error data to be
	spoken before Quinton's main functionality executes.
"""

import subprocess, json
from pathlib import Path
from time import sleep
from tinytag import TinyTag
from datetime import datetime
from typing import Union, Optional
#from omxplayer.player import OMXPlayer
from abc import ABCMeta # Used to differentiate custom warnings from custom exceptions

from . import audioplayer
from .config_src.config import Config
from .exceptions import (
	Error,
	Warn,
	AudioEncodingError,
	AudioPlaybackError
)

def speak(text: str, *, cfg: Config) -> bool:

	"""
		Speak error output to the user. This function works very similarly to
		`VoiceAssistant.speak()`. Returns `True` if the text was successfully
		spoken, `False` otherwise.
	"""

	success = False

	AUDIO_PATH = Path("../data/tmp/logspeech.wav")
	DATA_PATH = Path("../data/tmp/data.txt")

	subprocess.call(f"touch {str(AUDIO_PATH)}") # Create a path for the recording

	with open("../data/tmp/data.txt", "w") as data:
		data.write(text)

	output = int()

	# Save the reply to a file named using the unique identifer assigned to it
	#
	# Command line options (in order of usage):
	#	-v	 voice
	#	-s	 speed
	# 	-f	 file to read from (filename.txt)
	#	-w	 file to save to (filename.wav)
	#
	try:
		espeak_args = f"espeak -v {cfg.voice} -s {str(cfg.speed)} -f {str(DATA_PATH)} -w {str(AUDIO_PATH)}"
		output = subprocess.call(espeak_args, shell=True)
	except Exception:
		print(f"Encoding failed! (code: {output})")
		raise AudioEncodingError

		return success # `success` should be `False` here
	else:
		print(f"Encoding successful (code: {output})")

	# Play the audio
	try:
		audioplayer.play(str(AUDIO_PATH), pause=cfg.pause)
	except Exception:
		success = False
	else:
		success = True
	finally:
		return success

	# audiolen = TinyTag.get(AUDIO_PATH).duration # Get the duration of the recording of the reply

	# try:
	# 	player = OMXPlayer(AUDIO_PATH) # Play the recording

	# 	# Handle the potential case of `self.cfg.pause` being None
	# 	pause = float(cfg.pause if type(cfg.pause) is not None else 0)
	# 	sleep(audiolen + pause) # Allow the audio to finish playing before quitting, and add a little leeway
	# except Exception:
	# 	raise AudioPlaybackError
	# finally:
	# 	player.quit() # Exit the player

	# return success

def log(*, error: Union[Exception, Warning, Error, Warn], reason: str, code: int) -> dict:
	""" Log Quinton's error data to `../data/logs`. """

	LOG_PATH = Path("../data/logs")

	LOG_ENTRY = {
		"date": str,
		"error": str,
		"reason": reason,
		"result": str
	}

	logEntry = LOG_ENTRY.copy()

	# Determine the result of the error
	result = str()

	if issubclass(type(error), (Exception, Error)):
		result = "Aborted"
	elif issubclass(error, (Warning, Warn)):
		result = "Warning issued"

	# Update the empty info
	logEntry.update({
		"date": datetime.now().strftime("%F @ %T"),
		"error": str(error) if type(error) is ABCMeta else str(type(error)),
		"result": result
	})

	filename = logEntry.get("date").replace(" @ ", "_") + ".txt"

	with open(f"{LOG_PATH}/{filename}", "x") as logfile:
		# Write the dictionary to the log file
		for key, value in logEntry.items():
			logfile.write(f"{key}: {value}\n")
