#
# FILENAME: audioplayer.py | Quinton-VoiceAssistant
# DESCRIPTION: Functions to play audio to the user
# CREATED: 2020-12-31 @ 3:46 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Provides audio-output functionality using `ffplay` (`ffmpeg`) and `omxlayer`. """

import subprocess

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

def play(audiofile: str) -> int:
	""" Play some audio. Raises `extensions.AudioPlaybackError` upon failure. """

	try:
		output = subprocess.call(f"ffplay {__FFMPEG_OPTIONS} {audiofile}", shell=True)
	except Exception:


	
