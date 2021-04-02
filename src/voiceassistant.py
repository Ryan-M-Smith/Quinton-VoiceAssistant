#
# FILENAME: voiceassistant.py | Quinton-VoiceAssistant
# DESCRIPTION: The VoiceAssistant class
# CREATED: 2020-03-26 @ 2:25 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

""" Quinton's main functionality. """

import socket, pytz, random, pyowm, json
import subprocess, phonetics, sys, yaml

import speech_recognition as sr

from pathlib import Path, PosixPath
from time import sleep
from datetime import datetime
from typing import Union, Optional, Generator, NoReturn

#from omxplayer.player import OMXPlayer # Used to play audio
#from tinytag import TinyTag # Used to get audio duration

import audioplayer
from commandprocessor import CommandProcessor as cp
from config_src.config import Config
from config_src.permissions import Permissions as Perms
from livelisten import Listener
from exceptions import (
	MicrophoneWarning, WiFiWarning, AudioEncodingError,
	AudioPlaybackError, HistoryError, DataError, LocationError,
	TimezoneError, TimestampError, NoReplyError
)

class VoiceAssistant:
	"""
		The `VoiceAssistant` class holds a majority of the code for the voice assistant, controlling its primary
		functionality. It combines the necessary functions for speech recognition and processing, formulating
		replies, responding to the user, and everything else required to allow Quinton to run into one function
		(`VoiceAssistant.run()`) for the main function to call.
	"""

	# -----------------------------
	# NOTE: This section may need to be refactored to avoid a `with` statement at the class' top-level,
	# but this works for now.
	#
	# API Keys:
	# -----------------------------
	with open("../credentials.yaml", "r") as credentials:
		credsList = yaml.full_load(credentials)
		valList = list(credsList.get("credentials").values())

		# Houndify
		HOUNDIFY_ID = valList[0]
		HOUNDIFY_KEY = valList[1]
		# -----------------------
		# OpenWeatherMap
		OWM_KEY = valList[2]
		# -----------------------
	# -----------------------------

	# -------------------------------------------------------------------
	# NOTE: These variables and constants are currently unused.
	#
	# Data for calculating and storing Houndify credit usage information:
	# -------------------------------------------------------------------
	_unused_DAILY_CREDITS = 100 # The number of Houndify credits allotted per day
	_unused_used_credits = float()

	# The baseline number of credits required for the Houndify domains that a client is
	# registered under. Because Quinton is only registered under Speech-to-Text, and this
	# domain requires no credits, the value is 0.
	_unused_DOMAIN_CREDITS = 0

	_unused_CPS = 0.25 # For all audio queries, Houndify uses 0.25 credits per second of audio
	# -------------------------------------------------------------------

	recognizer = sr.Recognizer() # Recognizer class instance to listen for audio

	mic: sr.Microphone() = None # Microphone class instance
	isMuted: bool

	# Other class instances used to pass data into the `VoiceAssitant` class from other
	# classes
	cmdPsr = cp()
	cfg: Config
	perms: Perms
	listener: Listener

	def __init__(self, cfg: Config, perms: Perms) -> NoReturn:
		"""
			The `VoiceAssistant` class' constructor. Copies of the `Config` and
			`Permissions` classes are passed in so the `VoiceAssistant` class can access
			Quinton's configuration file and follow the user's allowed/denied permissions.
		"""

		self.cfg = cfg
		self.perms = perms
		self.listener = Listener(cfg=self.cfg)

		isMic = self.__getMicrophone()
		isWiFi = self.__checkWiFi()

		if not isMic:
			raise MicrophoneWarning

		if not isWiFi:
			raise WiFiWarning

		print("MICROPHONE TYPE:", type(self.mic))

	def __getMicrophone(self) -> bool:
		"""
			Searches through the filesystem's list of connected hardware devices for a microphone.
			Returns `True` if a microphone matching the given criteria is found.
		"""

		micname = str()

		try:
			# Search for a valid USB microphone in the listing
			for i, hwname in enumerate(sr.Microphone.list_microphone_names()):
				if ("USB" in hwname) or ("usb" in hwname):
					self.mic = sr.Microphone(device_index=i) # Choose the microphone
					micname = hwname
		except OSError:
			return False
		else:
			print(f"Microphone {micname} found.")
			return True

	@staticmethod
	def __checkWiFi() -> bool:
		"""
			Checks to see if the device is connected to the internet. Returns `True`
			if connected, `False` otherwise.
		"""

		HOME_IP = "127.0.0.1"

		try:
			ip = socket.gethostbyname(socket.gethostname())
		except Exception:
			return False
		else:
			if wifi := (ip != HOME_IP):
				print("Connected to internet")

			return wifi

	def run(self) -> NoReturn:
		"""
			Runs the voice assistant. This function follows the following process:

				1. Listen for the wake word
				2. Listen for user input (if the wake word is heard)
				3. Send the command to be processed
				4. Send the content dictionary's(ies') info to reply to the command and save the recording (if the user allows it)
				5. Speak the reply to the user OR play a reply from the cache

			This function will be executed infinitely as long as there are no errors.
		"""

		# NOTE: Future inclusion. Will eventually return `0` on success, non-zero otherwise.
		# Possible return codes for the function. Descriptions are given.
		# RETURN_CODES = [
		# 	0, # Normal exit
		# 	1, #
		# ]

		heardWakeWord = False

		while not heardWakeWord:
			heardWakeWord = self.__heardWakeWord() # Check if the wake word/phrase was uttered

			if heardWakeWord:
				break

		# Allow time for PyAudio to free the microphone so the SpeechRecognition library
		# can take over
		sleep(1.75)

		usrInput = self.listen() # Step 1

		(data, defaultData, dataFromCache) = self.cmdPsr.process(usrInput, perms=self.perms, time=self.__generateTimestamp()) # Step 2

		audioID = next(self.__genAudioIndex())

		if type(data) is dict:
			# Step 3
			(response, data) = self.__reply(data, backup=defaultData, dataFromCache=dataFromCache)

			if data.get("audio_index") == str():
				data.update({"audio_index": audioID})

				self.speak(response, audioID=audioID) # Step 4
			else:
				c_data = data.copy()
				(response, data) = self.__reply(c_data, backup=defaultData, dataFromCache=dataFromCache) # Alt step 3

				self.play(audioID=data.get("audio_index"), saveID=audioID) # Alt step 4 - Play the recording from the cache; Make private later
		else:
			# Handle a list of content dictionaries
			l_data = data.copy()
			(response, data) = self.__reply(l_data, backup=defaultData, dataFromCache=dataFromCache) # Alt step 3

			if data.get("audio_index") == str():
				data.update({"audio_index": audioID})

				self.speak(response, audioID=data.get("audio_index"))
			else:
				self.play(audioID=data.get("audio_index"), saveID=audioID) # Alt step 4

		self.__write(data=data, saveID=(audioID if data.get("from_cache") else None)) # Write the data

	def __generateTimestamp(self) -> datetime:
		""" Create a timestamp for Quinton's command history. """

		try:
			tz = pytz.timezone(self.cfg.timezone)
		except pytz.exceptions.UnknownTimeZoneError:
			raise TimezoneError

		time = datetime.now(pytz.timezone(tz.zone))

		fmt = "%Y-%m-%d %I:%M:%S %Z"

		loc_dt = tz.localize(datetime(time.year, time.month, time.day, time.hour, time.minute, time.second))

		return loc_dt.strftime(fmt)

	@staticmethod
	def __normalizeTime(time: str) -> str:
		""" Make Quinton read a time like a human would. """

		# The string indices will be a bit different if the hour is after 9
		pastNine = True if int(time[0] + time[1]) > 9 else False

		offset = 1 if pastNine else 0 # Index offset based on hour

		modTime = time # Will be changed and returned

		# Make a time like 5:08 be spoken as "five oh eight" instead of
		# "five zero eight"
		if (int(time[2 + offset]) == 0) and (int(time[3 + offset]) > 0):
			modTime = modTime.replace("0", "o")

		# Make a time like 5:00 be spoken as "five o'clock" instead of
		# "five zero zero"
		#
		# The range is 1-indexed, so if `time` equals "10 00", `time[1:2]` will
		# return '0' (i.e., (1, 2] in interval notation). Here, the indices 2 and 4
		# could be used (when offset is 0) or it could be 1 if the hour is past 9:00.
		try:
			if int(time[(2 + offset) : (4 + offset)]) == 0:
				modTime = modTime.replace("00", "o'clock")
		except ValueError:
			pass

		return modTime

	def listen(self) -> Optional[str]:
		""" Listens for the user's commands and returns the speech as text. """

		# Listen for speech commands
		if self.mic is not None:
			with self.mic as source:
				self.recognizer.adjust_for_ambient_noise(source)
				self.tone(4)

				audio = self.recognizer.listen(source, timeout=self.cfg.timeout, phrase_time_limit=self.cfg.time_limit)
		else:
			raise MicrophoneWarning

		self.tone(5)

		command = str()

		try:
			# Convert speech to text
			command = self.recognizer.recognize_houndify(audio, self.HOUNDIFY_ID, self.HOUNDIFY_KEY)
		except sr.UnknownValueError:
			print("Could not understand.")
		except sr.RequestError as e:
			print(f"Houndify error; {e}")
		except Exception as e: # Catchall
			print(f"Error: {e}")
		else:
			if command == "":
				command = None
				raise sr.UnknownValueError
		finally:
			return command.lower() if command is not None else command

	def __heardWakeWord(self) -> bool:
		""" Detect Quinton's wake word. Returns `True` if it's detected, `False` otherwise. """
		detectedPhrase = str()

		# Listen for the wake word
		try:
			print("Waiting for wake word...")

			# Record and check the decibel value of the wake word
			path = self.listener.liveListen()
			_, isInRange = self.listener.calcIntensity(audioPath=path)

			if isInRange:
				# Send the audio data to Houndify, but this time use the pre-recorded
				# audio file instead of live listenting. This will take the wave audio
				# from `../data/tmp/llout.wav` and turn it into the `speechrecognition.AudioFile`
				# type.
				wwphrase = sr.AudioFile(str(Path("../data/tmp/llout.wav")))

				with wwphrase as source:
					self.recognizer.adjust_for_ambient_noise(source)

					# Convert the `speechrecognition.AudioFile` into `speechrecognition.AudioData`. This type of
					# variable can be passed into the Houdify recognizer.
					audio = self.recognizer.record(source)

					# Detect the final phrase
					detectedPhrase = self.recognizer.recognize_houndify(audio, self.HOUNDIFY_ID, self.HOUNDIFY_KEY)
		except sr.UnknownValueError:
			detectedPhrase = None
		except sr.RequestError as e:
			print(f"Houndify error; {e}")
			detectedPhrase = None
		except Exception as e: # Catchall
			print(f"Error: {e}")
			detectedPhrase = None
		else:
			if detectedPhrase == "":
				detectedPhrase = None
			elif not detectedPhrase.islower():
				detectedPhrase = detectedPhrase.lower()
		finally:
			if (detectedPhrase != str()) and (detectedPhrase is not None):
				ww = self.cfg.wake_word.lower()

				# Check to see if the detected wake word matches the one in the config
				(match, struct) = self.__phoneticsCheck(wakePhrase=ww, detectedPhrase=detectedPhrase)

				if match:
					# Replace the detected phrase with the Soundex phonetic structure of the wake word
					# to detect its presence. By this point, it will be confirmed that the phonetic structure
					# of the two phrases (original and detected) are the same (and sound the same), even if they are
					# spelled slightly different
					structPhrase = detectedPhrase.replace(detectedPhrase, struct)

					return (struct in structPhrase) if all((structPhrase, detectedPhrase)) else False
				else:
					return False

	# The `*` is used because the function call isn't very readable without listing the parameters
	@staticmethod
	def __phoneticsCheck(*, wakePhrase: str, detectedPhrase: str) -> (bool, Optional[str]):
		"""
			Compares the phonetic structure of the user's wake word/phrase to a string recorded from
			the microphone using the Soundex Algorithm. This will help ensure that the wake word is
			detected, especially for wake words that don't sound the same as they are spelled. For
			example, "Quinton" sounds like "Quintin", and is detected as such by the `SpeechRecognition`
			library. Returns `(bool, Optional[str])` where `bool` is `True` if the phonetic structures of
			the two strings are the same, `False` otherwise. The phonetic structure of the wake word is
			returned only if `bool` is `True`. otherwise, `None` is returned here.
		"""

		if (wakePhrase is None) or (detectedPhrase is None):
			return (False, None)

		# Most wake words will have a word before the name, like "hey" or "ok". If this is
		# the case, separate the words before putting them through the Soundex algorithm because
		# the function can only take a single-word string.
		if (lenwp := len(wakePhrase.split())) > 1:
			wakePhrase = wakePhrase.split()

		if (lendp := len(detectedPhrase.split())) > 1:
			detectedPhrase = detectedPhrase.split()

		# Compare the number of words in the strings. This will help weed out any occurrences
		# where there is speech, but it has nothing to do with the wake word at all.
		if lenwp != lendp:
			return (False, None)

		# `structPhrase` is used for the structure of `wakePhrase`, while `structDPhrase`
		# is used for the structure of `detectedPhrase`. `structDPhrase` is only used if the
		# wake phrase has multiple words in it.
		structPhrase = structDPhrase = str()

		if type(wakePhrase) is list:
			# Get the phonetic structure of the wake phrase and the detected phrase
			for spword, sdpword in zip(wakePhrase, detectedPhrase):
				structPhrase += (phonetics.soundex(spword) + " ")
				structDPhrase += (phonetics.soundex(sdpword) + " ")

			structPhrase = structPhrase.strip()
			structDPhrase = structDPhrase.strip()

			if structPhrase == structDPhrase:
				return (True, structPhrase) # If the two values are equal, either one will have the correct structure
			else:
				return (False, None)
		else:
			if (struct := phonetics.soundex(wakePhrase)) == phonetics.soundex(detectedPhrase):
				return (True, struct)
			else:
				return (False, None)

	def __reply(self, commandInfo: Union[dict, list], *, backup: Optional[dict], dataFromCache: bool) -> (str, dict):
		"""
			Generates a reply to the user's query. A dictionary of content or a list
			of content dictionaries can be passed in.
		"""

		# Responses for Quinton if it can't do something or doesn't
		# understand the command.
		UNKNOWN = [
			"I'm sorry, I don't understand",
			"I'm not sure I understand"
		]

		if commandInfo is None:
			# Pick an "unknown" response
			try:
				if sys.version_info.minor > 8:
					random.seed()
				else:
					random.seed(datetime.now(tz=pytz.timezone(self.cfg.timezone)))
			except pytz.exceptions.UnknownTimeZoneError:
				raise TimezoneError

			return (random.choice(UNKNOWN), commandInfo)

		# Based on the type of data that is passed into the function, set it to its respective variable
		# to keep the naming neat ("l" denotes `list`, "d" denotes `dict`). For lists passed in, a sample
		# content dictionary is taken to determine what intent to reply to. In the case of a dictionary, this
		# variable will just be a copy of `commandInfo` (passed in data parameter).
		lCommandInfo = list()
		dCommandInfo = infoSample = dict()

		if type(commandInfo) is list:
			lCommandInfo = commandInfo
		else:
			dCommandInfo = commandInfo

		infoSample = commandInfo[0] if type(commandInfo) is list else commandInfo

		usingCache = False # Set to `True` if the cache is used
		filteredData = None

		try:
			timezone = pytz.timezone(self.cfg.timezone) # Get the timezone
		except pytz.exceptions.UnknownTimeZoneError:
			raise TimezoneError

		# Each type of command is assigned an ID number. For details about what each number
		# means, see `../doc/command-ids.md`.
		commandID = int()

		response: Optional[str] = None # THe response to the command

		if infoSample.get("intent") == "command":
			if ((("tell" in infoSample.get("keywords") or ("get" in infoSample.get("keywords"))) and ("weather" in infoSample.get("keywords"))) or ("weather" == infoSample.get("keywords"))): # Weather
				if not self.perms.canUseLocation:
					raise LocationError

				# Get information from OpenWeatherMap
				owm = pyowm.OWM(self.OWM_KEY)

				reg = owm.city_id_registry()
				idlist = reg.ids_for(city_name=self.cfg.city, country=self.cfg.country)
				obs = owm.weather_at_ids([idlist[0][0]])
				weather = obs[0].get_weather()

				# Create the reply
				if (self.cfg.units == "imperial") or (self.cfg.units == "metric"):
					unit = "fahrenheit" if self.cfg.units == "imperial" else "celsius"
				else:
					unit = "fahrenheit"

				temp = str(round(weather.get_temperature(unit=unit).get("temp")))

				response = f"{temp} degrees {unit.capitalize()} with {weather.get_detailed_status()}"

				if dataFromCache:
					content = lCommandInfo if type(commandInfo) is list else dCommandInfo # The content to be filtered
					search = response

					filteredData = self.cmdPsr.filterIrrelevant(content, search)

				if filteredData is not None:
					usingCache = True

				if not usingCache:
					commandID = 1
			elif ((("tell" in infoSample.get("keywords") or ("get" in infoSample.get("keywords"))) and ("time" in infoSample.get("keywords"))) and (infoSample.get("subject") == "user")): # Telling time
				# Get the current time
				time = datetime.now(pytz.timezone(timezone.zone))

				if dataFromCache:
					content = lCommandInfo if type(commandInfo) is list else dCommandInfo # The content to be filtered

					# When searching for a time, make sure to remove the leading zero from hours before 10 (A.M. or P.M.)
					#
					# TIME EDITING (Using 5:00 PM for the time)
					# time.strftime("%I %M %p") 	-> 05 00 PM
					# time.strftime("%I %M %p")[1:] -> 5 00 PM
					# time.strftime("%I %M %p")[:1] -> 05
					orig_time = time.strftime("%I %M %p")[1:] if int(time.strftime("%I %M %p")[:2]) < 10 else time.strftime("%I %M %p")

					search = self.__normalizeTime(orig_time)
					filteredData = self.cmdPsr.filterIrrelevant(content, search)

				if filteredData is not None:
					usingCache = True

				# If the cache isn't being used or no suitable content dictionaries are found,
				# a reply is generated.
				if not usingCache:
					commandID = 2

					orig_time = time.strftime("%I %M %p")[1:] if int(time.strftime("%I %M %p")[:2]) < 10 else time.strftime("%I %M %p")
					response = self.__normalizeTime(orig_time)
			elif (("tell" in infoSample.get("keywords") or ("get" in infoSample.get("keywords"))) and ("date" in infoSample.get("keywords"))):
				commandID = 3

				# Get the current date
				time = datetime.now(pytz.timezone(timezone.zone))
				dt = datetime.strptime((str(time.day) + "/" + str(time.month) + "/" + str(time.year)), "%d/%m/%Y")

				fmt = "%A, %B %d"

				response = dt.strftime(fmt)
			elif (("turn on" in infoSample.get("keywords")) and (infoSample.get("assets") is not None)): # Turn something on
				commandID = 4
				response = None
			elif (("turn off" in infoSample.get("keywords")) and (infoSample.get("assets") is not None)): # Turn something off
				commandID = 4
				response = None
			else:
				pass
		elif infoSample.get("intent") == "inquire":
			if (("what" in infoSample.get("question_words")) and ("weather" in infoSample.get("keywords"))): # Weather
				if not self.perms.canUseLocation:
					raise LocationError

				# Get information from OpenWeatherMap
				owm = pyowm.OWM(self.OWM_KEY)

				reg = owm.city_id_registry()
				idlist = reg.ids_for(city_name=self.cfg.city, country=self.cfg.country)
				obs = owm.weather_at_ids([idlist[0][0]])
				weather = obs[0].get_weather()

				# Create the reply
				if (self.cfg.units == "imperial") or (self.cfg.units == "metric"):
					unit = "fahrenheit" if self.cfg.units == "imperial" else "celsius"
				else:
					unit = "fahrenheit"

				temp = str(round(weather.get_temperature(unit=unit).get("temp")))

				response = f"{temp} degrees {unit.capitalize()} with {weather.get_detailed_status()}"

				if dataFromCache:
					content = lCommandInfo if type(commandInfo) is list else dCommandInfo # The content to be filtered
					search = response

					filteredData = self.cmdPsr.filterIrrelevant(content, search)

				if filteredData is not None:
					usingCache = True

				if not usingCache:
					commandID = 1
			elif ((("what" in infoSample.get("question_words")) and ("time" in infoSample.get("keywords"))) and ("is it" in infoSample.get("command"))): # Telling time
				# Get the current time
				time = datetime.now(pytz.timezone(timezone.zone))

				if dataFromCache:
					content = lCommandInfo if type(commandInfo) is list else dCommandInfo # The content to be filtered

					# When searching for a time, make sure to remove the leading zero from hours before 10 (A.M. or P.M.)
					#
					# TIME EDITING (Using 5:00 PM for the time)
					# time.strftime("%I %M %p") 	-> 05 00 PM
					# time.strftime("%I %M %p")[1:] -> 5 00 PM
					# time.strftime("%I %M %p")[:1] -> 05
					orig_time = time.strftime("%I %M %p")[1:] if int(time.strftime("%I %M %p")[:2]) < 10 else time.strftime("%I %M %p")

					search = self.__normalizeTime(orig_time)
					filteredData = self.cmdPsr.filterIrrelevant(content, search)

				if filteredData is not None:
					usingCache = True

				# If the cache isn't being used or no suitable content dictionaries are found,
				# a reply is generated.
				if not usingCache:
					commandID = 2

					orig_time = time.strftime("%I %M %p")[1:] if int(time.strftime("%I %M %p")[:2]) < 10 else time.strftime("%I %M %p")
					response = self.__normalizeTime(orig_time)
			elif (("what" in infoSample.get("question_words")) and (("is" in infoSample.get("to_be")) or ("what's" in ci.egt("full_command"))) and ("date" in infoSample.get("keywords"))): # Getting the date
				commandID = 3

				# Get the current date
				time = datetime.now(pytz.timezone(timezone.zone))
				dt = datetime.strptime((str(time.day) + "/" + str(time.month) + "/" + str(time.year)), "%d/%m/%Y")

				fmt = "%A, %B %d"

				response = dt.strftime(fmt)
			else: pass
		elif infoSample.get("intent") == "state":
			if infoSample.get("subject") == "user":
				if "favorite" in infoSample.get("keywords"):
					if dataFromCache:
						usingCache = True
					else:
						usingCache = False

					if not usingCache:
						objtype = objname = str()

						foundStart = foundEnd = False

						stopWords = infoSample.get("to_be") if infoSample.get("to_be") is not None else infoSample.get("articles")

						# Filter out parts of the command to look for a situation where the user tells
						# Quinton something about themself.
						for word in infoSample.get("command").split():
							if (not word in stopWords) and (not foundEnd):
								if word == "favorite":
									foundStart = True
									continue
								elif foundStart:
									objtype += word
							else:
								if not foundEnd:
									foundEnd = True

								if (not word in infoSample.get("articles")) and (not word in infoSample.get("to_be")):
									objname += word

						objtype = objtype.strip()

						# Get rid of plural nouns
						if objtype.endswith("s") or objtype.endswith("es"):
							objtype.rstrip("es") # Will take care of both cases

						if not foundEnd: # Not really necessary, as commandID is 0 by default
							commandID = 0
						else:
							infoSample.get("references").update({objtype: objname})

							commandID = 5
		else:
			pass

		if type(response) is str:
			response = response.strip()

		if (response is None) and (commandID != 5):
			raise NoReplyError

		# Use the backup content dictionary if all of the ones from the cache have
		# been filtered out.
		usingBackup = False

		if not usingCache:
			# Backup data is not sent from the command processor if the cache is not
			# used at the processing level.
			if dataFromCache:
				dCommandInfo = backup
				usingBackup = True
		else:
			commandInfo = filteredData

		if commandInfo is filteredData is lCommandInfo is dCommandInfo is backup is None:
			raise DataError

		# Each of these responses will be updated with the generated reply
		TEMPLATES = [
			f"ok, {response}",
			f"good {response}",
			f"It is {response}",
			f"It is currently {response}",
			f"Today is {response}",
			f"In {self.cfg.city}, it is currently {response}",
			"Got it",
			f"It's {response}",
			"Okay, I'll remember that"
		]

		UNABLE = [
			f"I'm sorry, {self.cfg.username}, I'm afraid I can't do that",
			"I'm unable to do that"
		]

		# NOTE: This dictionary might need renamed to avoid confusion with
		# `usable_replies` (declared below).
		USABLE_REPLIES = {
			0: None,
			1: [2, 3, 5],
			2: [2, 3, 7],
			3: [4],
			4: [0],
			5: [6, 8]
		}

		# The index numbers of the usable template replies for each ID number. For example ID 1 can
		# use `TEMPLATES[2]`, `TEMPLATES[3]`, and `TEMPLATES[5]` to talk about the weather, so 2, 3,
		# and 5 are appended to the list.
		usable_replies = USABLE_REPLIES.get(commandID)

		# Make sure all timestamps are up to date
		try:
			if (self.perms.canTimestampHist) and ("timestamp" in (infoSample if type(commandInfo) is list else commandInfo)):
				time = self.__generateTimestamp()

				if type(commandInfo) is list:
					for cdict in commandInfo:
						cdict.update({"timestamp": time})
				else:
					if (commandInfo.get("timestamp") == str()) or (commandInfo.get("timestamp") != time):
						commandInfo.update({"timestamp": time})
		except TypeError:
			raise TimestampError

		if response is usable_replies is None:
			if sys.version_info.minor > 8:
					random.seed()
			else:
				random.seed(datetime.now(tz=timezone))

			dCommandInfo.update({"reply": random.choice(UNABLE)})

			return (dCommandInfo.get("reply"), dCommandInfo)
		else:
			# If there are multiple replies for the query's command ID, pick a random one.
			# Otherwise, just use the one that's there. This way, `random.choice()`
			# doesn't waste time picking from only one reply template.
			if ((dCommandInfo == commandInfo) or usingBackup) and (not usingCache):
				if sys.version_info.minor > 8:
					random.seed()
				else:
					random.seed(datetime.now(tz=timezone))

				if len(usable_replies) > 1:
					dCommandInfo.update({"reply": TEMPLATES.copy()[random.choice(usable_replies)]})
				else:
					dCommandInfo.update({"reply": TEMPLATES.copy()[usable_replies[0]]})

				return (dCommandInfo.get("reply"), dCommandInfo) # Return for a single content dictionary
			elif (lCommandInfo == commandInfo) and (not usingCache):
				if sys.version_info.minor > 8:
					random.seed()
				else:
					random.seed(datetime.now(tz=timezone))

				# Pick a content dictionary to use. At this point, they all have the same intent and response,
				# so one is picked and given a full sentence reply.
				contDict = random.choice(lCommandInfo)

				if len(usable_replies) > 1:
					contDict.update({"reply": TEMPLATES.copy()[random.choice(usable_replies)]})
				else:
					contDict.update({"reply": TEMPLATES.copy()[usable_replies[0]]})

				return (contDict.get("reply"), contDict) # Return statement for many content dictionaries
			else:
				# Return data from the cache
				if type(filteredData) == dict:
					filteredData.update({"from_cache": True})

					return (filteredData.get("reply"), filteredData)
				elif type(filteredData) == list:
					if sys.version_info.minor > 8:
						random.seed()
					else:
						random.seed(datetime.now(tz=timezone))

					# Update the randomly chosen content dictionary to say that the data is from the cache,
					# and update the timestamp if applicable
					contDict = random.choice(filteredData)
					contDict.update({"from_cache": True})

					return (contDict.get("reply"), contDict)

	def speak(self, text: str, audioID: Optional[str] = None) -> NoReturn:
		""" Convert text to speech and speak the computer's reply. """

		AUDIO_PATH = Path("../data/cache/responses/" + str(audioID) + ".wav")
		DATA_PATH = Path("../data/tmp/data.txt")

		subprocess.call(f"touch {str(AUDIO_PATH)}", shell=True) # Create a path for the recording

		with open("../data/tmp/data.txt", "w") as data:
			data.write(text)

		# Save the reply to a file named using the unique identifer assigned to it
		#
		# Command line options (in order of usage):
		#	-v	 voice
		#	-s	 speed
		# 	-f	 file to read from (filename.txt)
		#	-w	 file to save to (filename.wav)
		#
		try:
			espeak_args = f"espeak -v {self.cfg.voice} -s {str(self.cfg.speed)} -f {str(DATA_PATH)} -w {str(AUDIO_PATH)}"
			output = subprocess.call(espeak_args, shell=True)
		except Exception:
			print(f"Encoding failed! (code: {output})")
			raise AudioEncodingError
		else:
			print(f"Encoding successful (code: {output})")

		audioplayer.play(str(AUDIO_PATH), pause=self.cfg.pause) # Play the audio

		if (not self.perms.canSaveToCache) or (audioID is None):
			# Delete the recording if the user doesn't want recordings to be saved or
			# if there is no passed in audio index.
			subprocess.call(f"rm {AUDIO_PATH}", shell=True)

	def play(self, audioID: str, saveID: str) -> NoReturn:
		"""
			Play a pre-recorded response from the cache, and then copy and resave it with a
			current audio index number.
		"""

		AUDIO_PATH = Path("../data/cache/responses/" + audioID + ".wav")

		audioplayer.play(str(AUDIO_PATH), pause=self.cfg.pause) # Play the audio

		# Resave the file if there were no errors
		subprocess.call(f"cp ../data/cache/responses/{audioID}.wav ../data/cache/responses/{saveID}.wav", shell=True)

	def tone(self, octave: int) -> int:
		""" Play a tone to let the user know when to speak. """

		code = 0

		if not octave in range(4, 6):
			code = 1
			return code

		TONE_PATH = Path("../audio")
		AUDIO_PATH: PostixPath

		 # C4 and C5 tones; the C4 is played to prompt the user to speak and the C5 is played
		 # before the command is processed/after the listening period ends.
		TONELIST = ["C4-261.63Hz.wav", "C5-523.25Hz.wav"]

		# Decide what octave of tone will be played
		AUDIO_PATH = Path(f"{str(TONE_PATH)}/{TONELIST[0] if octave == 4 else TONELIST[1]}")

		# Play the audio
		try:
			audioplayer.play(str(AUDIO_PATH), pause=self.cfg.pause)
		except Exception:
			code = 1
		else:
			code = 0
		finally:
			return code

	def __write(self, data: dict, saveID=None) -> NoReturn:
		""" Write Quinton's reply to a file, if the user allows it. """

		histPath = Path("../data/cache/history") # The JSON files with command history
		recPath = Path("../data/cache/responses") # The portion of the cache holding audio recordings
		memPath = Path("../data/memory/memory.yaml") # The YAML file with Quinton's "memory"

		# Depending on the situation, the command's audio index may not be able to be used because it
		# is the same as a previously saved audio file in the cache. In this case, use the save index -
		# an unused audio index that the cached response can point to.
		index = data.get("audio_index") if saveID is None else saveID

		if self.perms.canSaveToCache:
			# Create a history file that corresponds to an audio recording
			with open(str(histPath) + "/history-" + index + ".json", "x") as history:
				try:
					history.write(json.dumps(data, indent=4))
				except Exception:
					# Remove any empty or partially written history data. In addition, remove the corresponding
					# reply (if it exists)
					subprocess.call(f"rm {str(histPath)}/history-{index}.json", shell=True)
					subprocess.call(f"rm {str(recPath)}/{index}.wav", shell=True)

					raise HistoryError

		# Write any reference data to Quinton's memory. Serialize the data's
		# `references` dictionary as YAML and add it to the file. If the
		# dictionary is empty, nothing is written.
		if (data.get("references") is not None) and (len(data.get("references")) > 0) and (data.get("references") is not list):
			with open(str(memPath), "a+") as memfile:
				for key, value in data.get("references").items():
					if not f"{key}: {value}" in memfile.read():
						yaml.dump(data.get("references"), memfile)

	def __genAudioIndex(self) -> Generator[str, None, None]:
		"""
			Generate a unique, 6-character sequential identifier for each of Quinton's speech
			recordings.
		"""

		self.cfg.recordings += 1

		# Pad the number with leading zeros to get the length up to 6 places (e.g., 1 becomes 000001)
		yield str(self.cfg.recordings).zfill(6)

	def _unused_UpdateCredits(self, commandLen: float, wakeWord: int) -> NoReturn:
		"""
			[FUTURE] Update the amount of Houndify credits that have been used using Houndify's credit
			calculation formula (found at https://www.houndify.com/pricing#how-do-credits-work)
		"""

		self.used_credits += float((self.CPS * (commandLen + wakeWord)) + self.DOMAIN_CREDITS)


	def _unused_CreditsRemaining(self) -> (float, float):
		"""
			[FUTURE] Get the amount of Houndify credits used so far, and the amount remaining for
			the day.
		"""

		remaining = self.DAILY_CREDITS - self.used_credits
		return (self.used_credits, remaining)
