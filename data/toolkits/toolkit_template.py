#
# FILENAME: toolkit_template.py | Quinton-VoiceAssistant
# DESCRIPTION: A sample ToolKit
# CREATED: 2020-11-21 @ 3:37 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

import sys
import pytz # Timezone stuff
from typing import Union, Optional # If you want to remove type annotations, you don't need these
from datetime import datetime # For seeding based on time

class ToolKit:
	""" 
		A template ToolKit. Any user-generated ToolKit should be in a class derived from this
		class.
	"""

	#
	# Keywords
	#
	# Put any of your new keywords in their respective lists.
	# If you need to add something different, such as a question word,
	# see `../commandprocessor.py`.
	#

	KEYWORDS = []

	# Multi-word keywords
	CMPD_KEYWORDS = [
		# Example: "turn on",
	]

	# Alternate keywords
	ALT_KEYWORDS = [
		# Examples:
		# "like",
		# "favorite"
	]

	# Any assets you might need to add
	ASSETS: dict = {
		# Example: "bedside-lamp": "lamp",
	}

	# Needs to mimic the `VoiceAssistant.reply()` function
	def reply(self, commandInfo: Union[dict, list], *, backup: Optional[dict], dataFromCache: bool) -> (str, dict):
		"""
			This is where you will generate replies for a command. Your code will need to have a way to process either a single
			command (in the form of a single content dictionary), or multiple commands (in the form of a list of content dictionaries).
			Your code will also need to be able to handle a backup dictionary if no data from the cache can be matched to the command. 
		"""

		# Some necessary variables to be used later. Copy and pase lines 54-98.

		# Each type of command is assigned an ID number. For details about what each number 
		# means, see `../doc/command-ids.md`.
		commandID = int()

		# The index numbers of the usable template replies for each ID number. For example ID 1 can
		# use `TEMPLATES[2]`, `TEMPLATES[3]`, and `TEMPLATES[5]` to talk about the weather, so 2, 3, 
		# and 5 are appended to the list.
		usable_replies = list()

		# Your response goes in this variable. Each reply case will need to eventually set this
		# variable to something.
		response: Optional[str] = None

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
					# You don't have to seed with `pytz`; I just decided to. `None` or some other
					# method will work just as well.
					random.seed(datetime.now(tz=pytz.timezone(self.cfg.timezone)))
			except pytz.exceptions.UnknownTimeZoneError:
				pass # Do whatever you want here; VoiceAssistant.reply() raises a custom exception.

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

		# If your ToolKit will need information about the time, you probably need the following lines.
		# Otherwise, ignore lines 106-109
		try:
			timezone = pytz.timezone(self.cfg.timezone) # Get the timezone
		except pytz.exceptions.UnknownTimeZoneError:
			pass # Again, do whatever you want here; VoiceAssistant.reply() raises a custom exception.
	
	#
	# THIS IS WHERE YOUR CODE GOES.
	#
	# Here, you will write the logic for filtering your custom commands using your custom-defined keywords.
	# For ideas on what your logic could look like, feel free to borrow from `voiceassistant.py` in the `src`
	# directory.
	#
