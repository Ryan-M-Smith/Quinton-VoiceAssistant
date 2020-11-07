#
# FILENAME: exceptions.py | Quinton-VoiceAssistant
# DESCRIPTION: User-defined exceptions raised by the voice assistant in certain conditions
# CREATED: 2020-05-09 @ 11:11 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Custom exceptions and warnings. """

# NOTE: Currently, "warnings" (i.e., subclasses of `Warn`) are being treated as exceptions
# because in Quinton's current state (no GUI setup wizard/control panel), it would be difficult
# to 

from abc import ABC # For creating abstract base classes
from sys import version_info

# A note about error codes
#
# * Error codes are either in the 100s or 200s (depending on the type of error),
# 	will show up in log files, and are used as the exit code parameter for the
#	`exit()` function in the case of an exception
#
# * `Error` and `Warn` are the superclasses of all of the custom errors, so
#	 they are assigned codes 100 and 200, respectively. These codes will likely
#	 never show up anywhere.
#
# * Error codes are given to each error type alphabetically, and exception
#	codes are independent of warning codes. This is why the exceptions
# 	are numbered up to 111, and the warnings only go up to 205. 

class Error(ABC, Exception):
	""" The abstract base class for all of the other custom exceptions. """
	reason = str()
	code = 100 # All exit codes for exceptions are in the 100s

class Warn(ABC, Warning):
	""" The abstract base class for all of the other custom warnings. """
	reason = str()

	# All exit codes for exceptions are in the 200s. A warning will never abort
	# program execution, so warning codes will only show up in logs.
	code = 200

	@classmethod
	def getSubclasses(cls) -> dict:
		""" 
			Get the subclasses of the class. The subclasses are returned in a
			common form to help with comparison to caught exceptions. A dictionary
			with the common name mapped to the original type is returned.
		"""

		returnDict = dict()

		# Take the list of subclasses of the `Warn` class and convert the type name
		# (in the form `<class 'exceptions.ClassName'>`) to the form "`exceptions.Classname`".
		# The resulting tuple of strings will be easier to work with, and will be easier to compare
		# to warnings raised by other functions.
		for subclasses in cls.__subclasses__():
			returnDict.update({str(subclass).strip("<>").split()[1].strip("\'"): t})

		return returnDict

class AudioEncodingError(Error):
	""" Quinton failed to convert text to speech. """
	reason = "Audio encoding from text to speech failed. Aborting."
	code = 101

class AudioPlaybackError(Error):
	""" Quinton failed to play back the recording of its response. """
	reason = "Audio playback failed. Aborting."
	code = 102

class CacheIntentError(Error):
	""" 
		There was a problem unifying the intents of content dictionaries from the cache.
		In addition, `statistics.StatisticsError` was most likely raised.
	"""
	reason = "There was a problem unifying the intents of content dictionaries from the cache. " + \
			 "A cache clear will be done and then a reset. Aborting."
	code = 103

class ConfigFileWarning(Warn):
	""" The user config file is missing, corrupted, or can't be read. """
	reason = "Configuration failed. Reverting to the default configuration file."
	code = 201

class CountryCodeError(Error):
	""" The country code entered in Quinton's configuration file doesn't meet the critera. """
	reason = "The country code entered in Quinton's configuration file doesn't meet the critera. " + \
			 "It must be a two-character identifier. Aborting."
	code = 104

class DataError(Error):
	""" There are no content dictionaries (including backups) for a command. """

class DefaultConfigError(Error):
	""" The default config file is missing, corrupted, or can't be read. """
	reason = "Configuration through the default configuration file failed. Aborting."
	code = 105

class HistoryError(Error):
	""" The process of saving of the Python dictionary containing JSON command output failed. """
	reason = "Saving the history from the command failed. Aborting."
	code = 106

class LocationError(Error):
	""" There was a problem accessing the user's location. """
	reason = "There was a problem accessing your location. Please allowed me to access your " + \
			 "location in the configuration file."
	code = 107

class MicrophoneWarning(Warn):
	""" No microphone connected or recognized. """
	reason = "There is no microphone connected. Please connect a microphone to continue."
	code = 202

class NoReplyError(Error):
	""" A content dictionary had a reply as `None`. """
	reason = "Reply was nonexistant. Aborting."
	code = 108

class NotUnderstood(Warn):
	""" Spoken command not understood. """
	pass # Uses randomly picked custom responses defined elsewhere

class PyVersionError(Error):
	""" The user is running the software with an outdated version of Python. """

	# Have the "." be read as "point"
	reason = f"You are currently running python version {version_info.major}.{version_info.minor}.{version_info.micro}, but " + \
			  "Python version 3.8 or above is required. Please upgrade and try again.".replace(".", " point ", 3)
	code = 109

class RequestLimit(Error):
	""" [FUTURE INCLUSION] The user has used up all of their available credits for the day. """
	reason = "You've used up all of your Houndify credits for the day."
	code = 110

class SetupWarning(Warn):
	""" 
		[FUTURE INCLUSUION] The user hasn't set up Quinton with the config software. Because this
		exception has no use in current versions of `Quinton-VoiceAssistant`, it is removed from 
		the final releases.
	"""
	reason = "Please set up Quinton through the Quinton config software."
	code = 203

class TimestampError(Error):
	""" Something went wrong while updating the command timestamp. """
	reason = "An error occurred while timestamping a command. Aborting."
	code = 111

class TimezoneError(Error):
	""" Something when wrong when `pytz` tried to load the timezone information. """
	reason = "Loading timezone information failed. Please make sure your timezone is valid. Aborting."
	code = 112

class WiFiWarning(Warn):
	""" No Wi-Fi connection. """
	reason = "There is no Wi-fi connection. Please connect to Wi-fi to continue."
	code = 204

class UnknownProblem(Warn):
	"""
		Something went wrong during Quinton's execution. \n
		This is most likely due to to a Python exception being raised (`TypeError`, `OSError`, `ValueError`, etc.). 
		The problem may have just been a one-time thing, or it may be a recurring bug.
	"""
	reason = "Something went wrong during execution. Returning to listening mode."
	code = 205