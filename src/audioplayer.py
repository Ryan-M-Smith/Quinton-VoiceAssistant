#
# FILENAME: audioplayer.py | Quinton-VoiceAssistant
# DESCRIPTION: Functions to play audio to the user
# CREATED: 2020-12-31 @ 3:46 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Provides audio-output functionality using `ffplay` (`ffmpeg`) and `omxlayer`. """

import subprocess
from typing import NoReturn
from omxplayer.player import OMXPlayer # Used to play audio
from tinytag import TinyTag # Used to get audio duration

from exceptions import AudioPlaybackError

# Command line options to pass to `ffplay` (in order of appearance):
#
# ---------------------------------------------------------------------------------
# COMMAND 		  |	 DESCRIPTION
# ---------------------------------------------------------------------------------
# -nodisp		  |	 Don't display the `ffplay` GUI window
# ---------------------------------------------------------------------------------
# -autoexit		  |	 Automatically quit `ffplay` when the file is finished playing
# ---------------------------------------------------------------------------------
# -nostats		  |	 Hide playback statistics
# ---------------------------------------------------------------------------------
# -hide_banner	  |	 Supress copyright and version info
# ---------------------------------------------------------------------------------
# -loglevel fatal |	 Only display fatal errors that cause `ffplay` to crash 
# ---------------------------------------------------------------------------------
#
__FFMPEG_OPTIONS = "-nodisp -autoexit -nostats -hide_banner -loglevel fatal"

def play() -> NoReturn:
	""" Play some audio. This will either use `ffmpeg` or `omxplayer` (if you're running 
		on a Raspberri Pi).
	"""
	if os.path.exists("/usr/bin/omxplayer"):
		__omxplay(str(AUDIO_PATH), pause=self.cfg.pause)
	else:
		__ffplay(str(AUDIO_PATH), pause=self.cfg.pause)

def __ffplay(audiofile: str) -> int:
	""" Play audio using `ffmpeg`. Raises `extensions.AudioPlaybackError` upon failure. """

	try:
		output = subprocess.call(f"ffplay {__FFMPEG_OPTIONS} {audiofile}", shell=True)
	except Exception:
		raise AudioPlaybackError
	finally:
		return output

def __omxplay(audiofile: str, pause: float) -> int:
	""" 
		Play audio using `omxplayer`. Raises `extensions.AudioPlaybackError`
		upon failure.
	"""

	audiolen = TinyTag.get(audiofile).duration # Get the duration of the recording of the reply

	try:
		player = OMXPlayer(audiofile) # Play the recording

		# Handle potential errors with the pause being None.
		full_pause = audiolen + float(pause if type(pause) is not None else 0)
		sleep(full_pause) # Allow the audio to finish playing before quitting, and add a little leeway
	except Exception:
		raise AudioPlaybackError
	finally:
		player.quit() # Exit the player
	
