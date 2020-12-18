#
# FILENAME: commandprocessor.py | Quinton-VoiceAssistant
# DESCRIPTION: The CommandProcessor class
# CREATED: 2020-03-26 @ 3:50 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Manipulate a command and collect content dictionaries from the cache. """

import random, sys, os
from datetime import datetime
from typing import Union, Optional, Any
from statistics import mode, StatisticsError

from cache_src.history import History
from config_src.permissions import Permissions as Perms
from exceptions import CacheIntentError, ToolKitLoadError

class CommandProcessor:
	"""
		Collects data from a command (spoken or otherwise), organizes it, and returns it to the VoiceAssistant class. 
		Commands are separated out into question words, keywords, intent of the command, referenced subjects, referenced 
		assets (smart devices the assistant can control), and two versions of the spoken command: one with the original formatting, 
		and one with only alphanumeric characters. The two versions of each command are only different if the command comes in 
		the form of a string typed by a user (as opposed to a string from a spoken command).
	"""

	histRef = History() # A way for the CommandProcessor class to access the command history

	# Recognized keywords
	KEYWORD_LIST = [
		"time",
		"weather",
		"location",
		"place",
		"set",
		"activate",
		"from",
		"left",
		"date",
		"day",
		"tell",
		"get"
	]

	CMPD_KEYWORDS = [
		"turn on",
		"turn off"
	]

	# Informal keywords which, in certain cases, may be used in a statement instead of 
	# a command. Some of these alternate keywords are the same as some command-oriented 
	# keywords and will only be recognized once when enumerating over the command. Many 
	# of these keywords are associated with giving the voice assistant facts about onesself 
	# for it to remember.
	ALT_KEYWORDS = [
		"time",
		"like",
		"favorite"
	]

	# Recognized question words
	QUESTION_WORD_LIST = [
		"what",
		"when",
		"which",
		"how",
		"why",
		"where",
		"who",
		"whose"
	]

	# Recognized compound question words
	CMPD_QSTN_WORDS = [
		"how much",
		"how many",
		"at what"
	]

	# Possible intents of the user
	INTENTS = [
		"state",
		"command",
		"inquire"
	]

	# Extra conjunctions, verbs, and prepositions (currently not being used, possibly in the future)
	AUXILLARY: list = None #[
		# "so",
		# "and",
		# "or",
		# "but",
		# "with",
		# "to"
	#]

	TO_BE = [
		"am",
		"is",
		"are"
	]

	# The subject, recipient or target audience of a command
	SUBJECTS = {
		"I": None,
		"me": ["my", "mine"],
		"you": ["your"]
	}

	# NOTE: Future inclusion
	# Assets that can be controlled by the voice assistant. Their proper name will
	# be mapped to their alias, allowing the alias to be used when speaking.
	if sys.version_info.minor >= 9:
		ASSETS = {
			"bedside-lamp": "lamp",
			"ceiling-light": "light"
		}
	else:
		ASSETS = dict({
			"bedside-lamp": "lamp",
			"ceiling-light": "light"
		}, **assets)

	ARTICLES = [
		"the",
		"a",
		"and"
	]
 
	def process(self, command: str, *, perms: Perms, time: str) -> (Optional[Union[dict, list]], Optional[dict], bool):
		"""
			Processes a spoken command, and detects:
				- Question words
				- Keywords
				- Intent
				- Subject
				- Assets
				- Two variations of the command

			
			Returns a three-element tuple:
			
			Element 1: A content dictionary (content pulled from the spoken command) 
			or a list of content dictionaries from the cache that match the command. If there 
			is only one content dictionary that matches the spoken command, a single dictionary 
			is returned.

			Element 2: An optional backup content dictionary. This way, if all
			of the content dictionaries in the cache are filtered out, a reply can still be generated.

			Element 3: A boolean value which tells other functions whether or not the main data (element 1) returned
			from this function is from the cache.  
		"""

		full_command = command # A version of the command with all characters and original capitalization (only used in the CLI version)

		returnDict = {
			"timestamp": (time if perms.canTimestampHist else None), # Will be removed if the user doesn't want a timestamp
			"question_words": list(),
			"keywords": list(),
			"to_be": list(),
			"articles": list(),
			"intent": str(),
			"subject": str(),
			"assets": list(),
			"references": dict(), # Anything a user references while speaking. Type of item is mapped to the item's name (e.g., "animal": "dog").
			"full_command": full_command,
			"command": command,
			"reply": str(), # Will be entered once it's determined later down the line
			"audio_index": str(),
			"save_index": str(), # Will be removed if the data isn't from the cache
			"from_cache": False
		}

		# Remove the timestamp key-value pair all together if it isn't needed. This will get rid 
		# of clutter, and it isn't really helpful to see a `"timestamp": null` pair in the history file
		# if the user didn't want a timestamp. In other words, they don't really need to see this if it's
		# not being used.
		if returnDict.get("timestamp") is None:
			returnDict.pop("timestamp")

		if returnDict.get("full_command") is None:
			c_returnDict = returnDict.copy()
			c_returnDict = None
			return (c_returnDict, None, False)
		
		# Keep all characters one case for easier processing
		if not command.islower():
			command = command.lower()

		# Remove non-alphanumeric characters from the simplified command
		if not command.isalnum():
			for i in command:
				if (not i.isalnum()) and (not i.isspace()):
					command = command.replace(i, "", count=1)
		
		returnDict.update({"command": command})
		
		# Check the history for a previous instance of the same command. Finding pre-responded commands
		# in the cache will speed up processing and skip the reply step, allowing commands to be responded 
		# to faster. This is skipped entirely if the user has opted not to save data to the cache.
		if perms.canSaveToCache:
			(found, idList, dataList) = self.histRef.search(command)

			if (found) and (idList is not None) and (dataList is not None):
				# Filter by intent and return possible content dictionaries for the query, 
				# along with the incomplete backup content dictionary.

				# A modified version of a cache content dictionary, not from the cache,
				# and without a reply or audio index. This will be like a backup content
				# dictionary if all of the options from the cache are filtered out.
				
				# A basic backup - no timestamp
				if sys.version_info.minor >= 9:
					basic = dataList[0] | {"reply": str(), "audio_index": str(), "from_cache": False}
				else:
					basic = dict(
						dataList[0], 
						**{
							"reply": str(), 
							"audio_index": str(), 
							"from_cache": False,
						}
					)
				
				timestamped = (basic | {"timestamp": time}) if sys.version_info.minor >= 9 else dict(basic, **{"timestamp": time})

				backup = timestamped if perms.canTimestampHist else basic # Timestamped option added here

				return (self.__filterIntent(dataList), backup, True)

		# If nothing suitable is found after searching the cache, or the cache is
		# not being used, a new command reply is generated.

		returnDict.pop("save_index")

		#
		# [--- PROCESSING STEP 1: Filter out keywords ---]
		#

		# Start as `False`; if any of these words are found, their respective 
		# variables will be set to `True`
		foundKeywords = False
		foundAltKwds = False
		foundQstWords = False
		foundToBe = False
		foundArticles = False
		
		# The words found in the command. If any are found, they are appended to
		# their respective lists.
		commandKeywords = list()
		commandAltKwds = list()
		commandQstWords = list()
		to_be = list()
		articles = list()
		
		# These are special lists that will hold compound words until they can be
		# combined with the others. These lists will not be used as part of the return 
		# dictionary.
		commandCmpdQWords = list()
		commandCmpdKWords = list()

		# Check to see if the picked up command contains any keywords related to
		# a command
		for _, keyword in enumerate(self.KEYWORD_LIST):
			# Search for keywords, with the command matching the case of the list
			if keyword in command.split(): # Use `command.split()` to search for an exact string
				if not foundKeywords:
					foundKeywords = True
				
				commandKeywords.append(keyword)
		
		# When adding the keywords, also check for alternate keywords and compound keywords
		
		# Alternate
		for _, altkwd in enumerate(self.ALT_KEYWORDS):
			# Add any non-command-oriented keywords to the list while avoiding duplicates  
			if (altkwd in self.KEYWORD_LIST) and (altkwd in commandKeywords):
				continue
			
			if altkwd in command.split():
				if not foundAltKwds:
					foundAltKwds = True
				
				commandAltKwds.append(altkwd)

		# Compound
		for _, ckeyword in enumerate(self.CMPD_KEYWORDS):
			if ckeyword in command: # Don't split here to detect multi-word keywords
				if not foundKeywords:
					foundKeywords = True
			
				commandCmpdKWords.append(ckeyword)
		
		# Combine all of the question words together into one list
		commandKeywords += commandCmpdKWords

		# Repeat the same procedure to find question words. Once 
		# for non-compound and again for compound question words.
		for _, qstword in enumerate(self.QUESTION_WORD_LIST):
			# Search for question words, with the command matching the 
			# case of the list
			if qstword in command.split():
				if not foundQstWords:
					foundQstWords = True
				
				commandQstWords.append(qstword)
		
		for _, cqstword in enumerate(self.CMPD_QSTN_WORDS):
			if cqstword in command: # Don't split here to detect multi-word question words
				if not foundQstWords:
					foundQstWords = True

				# Because the word "how" will only show up in this loop if it is part of
				# a compound question word ("how much", "how many"), "how" by itself can 
				# be removed so multiple question words containing "how" are not recognized 
				# in the same command. Use the same reasoning to differentiate "what" from
				# "at what".
				if ("how" in commandQstWords) and ("how" in cqstword):
					commandQstWords.remove("how")

				if ("what" in commandQstWords) and ("what" in cqstword):
					commandQstWords.remove("what")
				
				# Append to a separate list for joining later
				commandCmpdQWords.append(cqstword)
		
		for _, word in enumerate(self.TO_BE):
			if word in command.split():
				if not foundToBe:
					foundToBe = True
				
				to_be.append(word)
		
		for _, word in enumerate(self.ARTICLES):
			if word in command.split():
				if not foundArticles:
					foundArticles = True
				
				articles.append(word)

		
		# Combine all of the question words together into one list
		commandQstWords += commandCmpdQWords
		
		if not foundKeywords:
			# If there are no keywords, there can't be any compound
			# keywords either.
			commandKeywords = commandCmpdKWords = None

		# Set the alternate keywords separately because they can exist without
		# command keywords being present.
		if not foundAltKwds:
			commandAltKwds = None

		if not foundQstWords:
			# Follow the same logic for question words
			commandQstWords = commandCmpdQWords = None

		if not foundToBe:
			to_be = None
		
		if not foundArticles:
			articles = None

		#
		# [--- PROCESSING STEP 2: Store recognized keywords ---]
		#

		# Split the command to pull out important words
		tokens = command.split()

		# Modify the tokens to accept compound question words as one token
		if commandCmpdQWords is not None:
			for i, _ in enumerate(tokens):
				if (tokens[i] == "how") or (tokens[i] == "at"): # Check for first portion of the compound word
					if (tokens[i+1] == "much") or (tokens[i+1] == "many") or (tokens[i+1] == "what"): # Check for the second portion
						# Verify that the attempted modification is a recognized compound
						# question word
						if (tokens[i] + " " + tokens[i+1]) in self.CMPD_QSTN_WORDS:
							tokens[i] += (" " + tokens[i+1]) # Add the second portion to the first
							tokens.remove(tokens[i+1]) # Remove the old second portion
						else: 
							continue
		
		# Modify the tokens to accept compound keywords as one token
		if commandCmpdKWords is not None:
			for i, _ in enumerate(tokens):
				if tokens[i] == "turn": # Check for first portion of the compound word
					if (tokens[i+1] == "on") or (tokens[i+1] == "off"): # Check for the second portion
						# Verify that the attempted modification is a recognized compound
						# keyword
						if (tokens[i] + " " + tokens[i+1]) in self.CMPD_QSTN_WORDS:
							tokens[i] += (" " + tokens[i+1]) # Add the second portion to the first
							tokens.remove(tokens[i+1]) # Remove the old second portion
						else: 
							continue
		
		# Add the lists of recognized words to the dictionary being returned

		if commandQstWords is not None:
			returnDict["question_words"] = commandQstWords
		
		# Keywords are added separately based on type and value
		if commandKeywords is not None:
			returnDict["keywords"] += commandKeywords 
		
		if commandAltKwds is not None:
			returnDict["keywords"] += commandAltKwds

		if to_be is not None:
			returnDict["to_be"] = to_be
		
		if articles is not None:
			returnDict["articles"] = articles
		
		# Catchalls
		if ((rdqw := returnDict["question_words"]) is not None) and (len(rdqw) == 0):
			returnDict["question_words"] = None

		if ((rdkw := returnDict["keywords"]) is not None) and (len(rdkw) == 0):
			returnDict["question_words"] = None
		
		if ((tobe := returnDict["to_be"]) is not None) and (len(tobe) == 0):
			returnDict["to_be"] = None
		
		if ((artc := returnDict["articles"]) is not None) and (len(artc) == 0):
			returnDict["articles"] = None

		#
		# [--- PROCESSING STEP 3: Determine intent ---]
		#

		intent = str()

		# If the intent is to ask a question ("inquire"), the command will most
		# likely start with a question word. Search for any of these, as well as 
		# the compound ones. There is also a possibility of a question being formed
		# a different way. This is checked as well. Commands and statements are determined
		# based on the type of keywords used. 
		
		for ps in range(2):
			if ps == 0:   
				if commandQstWords is not None: # Easiest check to find a question
					if tokens[0] in commandQstWords:
						intent = "inquire"
				elif commandCmpdQWords is not None:
					if tokens[0] in commandQstWords:
						intent = "inquire"
				elif tokens[0] in self.TO_BE:
					intent = "inquire"
			elif ps == 1:
				# Based on the keywords, if any, in the command, determine whether the
				# intent is to "command" or "state".

				if (commandKeywords is not None) and (commandAltKwds is None):
						intent = "command"
				else:
					intent = "state"
			else: pass

			if intent != "":
				break # Once the intent is found, move on
		
		if intent == "":
			intent = "unknown" # Intent couldn't be determined

		returnDict["intent"] = intent

		#
		# [--- PROCESSING STEP 4: Determine subject ---]
		#

		foundSubject = False

		subject = str()

		for _, it_subject in enumerate(self.SUBJECTS):
			if it_subject in command: # Iterate through the main list of subjects
				if not foundSubject:
					foundSubject = True

				subject = it_subject
			else: # Iterate through the alternate forms of a subject, if applicable
				if self.SUBJECTS.get(it_subject) is not None:
					for _, sub_form in enumerate(self.SUBJECTS.get(it_subject)):
						if sub_form in command:
							if not foundSubject:
								foundSubject = True
							
							subject = sub_form
		
		if (not foundSubject) and (intent != "command"):
			subject = "unknown"
		else:
			if intent == "command":
				subject = "you"

		# Change the subject to be from the computer's point of view
		if intent != "unknown":
			for _, it_subject in enumerate(self.SUBJECTS):
				if it_subject == subject:
					if (subject == "I") or (subject == "me"):
						subject = "user"
					elif (subject == "you"):
						subject = "computer"
				else: # Iterate through the alternate forms of a subject, if applicable
					if self.SUBJECTS.get(it_subject) is not None:
						for _, sub_form in enumerate(self.SUBJECTS.get(it_subject)):
							if subject == sub_form:
								if (subject == "my") or (subject == "mine"):
									subject = "user"
								elif subject == "your":
									subject == "computer"

		returnDict["subject"] = subject

		#
		# [--- PROCESSING STEP 5: Find Assets ---]
		#

		foundAssets = False

		commandAssets = []

		for _, asset in enumerate(self.ASSETS):
			if self.ASSETS.get(asset) in command: # Search for asset aliases in the command
				if not foundAssets:
					foundAssets = True
				
				commandAssets.append(asset) # Append the full name, not the alias

		if not foundAssets:
			commandAssets = None

		returnDict["assets"] = commandAssets

		#
		# [--- Return the output ---]
		#
		return (returnDict.copy(), None, False)
	
	@staticmethod
	def __filterIntent(dataList: list) -> Optional[Union[dict, list]]:
		""" 
			Filter a passed-in list of content dictionaries from the cache to make sure 
			they all have the same intent. Content dictionaries without the correct intent
			are removed from the list and can't be returned. These content dictionaries are
			unusable because intent is important once a query is replied to. This is especially 
			true for queries about the time, because a statement ("tell me the time") is different
			from a question ("what time is it?").
		"""
		
		dl = dataList.copy()

		# Make sure all content dictionaries have the same intent.
		intents = list()
		freqIntent = str() # Most frequent intent 

		# Step 1: Get the intents of all of the content dictionaries in `dl`
		intents = [cdict.get("intent") for cdict in dl]

		# Step 2: Find the most frequent intent
		try:
			freqIntent = str(mode(intents))
		except StatisticsError:
			raise CacheIntentError	
		
		# Filter the content dictionaries that don't share the "mode" intent
		dl = [cdict for cdict in dl if cdict.get("intent") == freqIntent]

		if len(dl) == 0:
			dl = None

		# Return a single dictionary if there is only one item in `dl`; otherwise, 
		# return the whole list. `None` is returned if dl is `None`.
		return (dl if len(dl) > 1 else dl[0]) if (dl is not None) else None
	
	@staticmethod
	def filterIrrelevant(data: Optional[Union[dict, list]], search: Any) -> Optional[Union[dict, list]]:
		""" 
			Filter one or more content dictionaries with the same intent to remove replies that
			are wrong or irrelevant. For example, when asking for the weather on a rainy day, any
			results with the incorrect result (say, sunny) are filtered out. One or more content
			dictionaries are returned, but it is also possible for there to be no matches, in which
			case `None` is returned.
		"""
		relevantContent = list() # Not used if only one content dictionary is passed in

		if data is None:
			return None
		
		if type(data) is list:
			# For a list of content dictionaries
			for i, cdict in enumerate(data):
				if search in cdict.get("reply"):
					relevantContent.append(cdict)
		else:
			# For a single content dictionary
			return data if search in data.get("reply") else None
		
		if len(relevantContent) > 0:
			return relevantContent[0] if len(relevantContent) == 1 else relevantContent
		else:
			return None
