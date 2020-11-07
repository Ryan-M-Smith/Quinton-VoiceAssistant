# FILENAME: ifalgtest.py
# DESCRIPTION: Test Quinton's intent-filtering algorithm

from statistics import mode, StatisticsError

def sort_algorithm(dataList: list):
	""" Sort the intents of Quinton's content dictionaries. """

	intents = list()
	freqIntent = str() # Most frequent intent 

	# Step 1: Get the intents of all of the content dictionaries in `dataList`
	intents = [cdict.get("intent") for cdict in dataList]

	# Step 2: Find the most frequent intent
	try:
		freqIntent = str(mode(intents))
		print(f"freqIntent: {freqIntent}")
	except StatisticsError:
		raise CacheIntentError	
	
	# Filter the content dictionaries that don't share the "mode" intent
	dataList = [cdict for cdict in dataList if cdict.get("intent") == freqIntent]

	if len(dataList) > 0:
		# Return a single dictionary if there is only one item in `dataList`,
		# otherwise, return the whole list
		return dataList if len(dataList) > 1 else dataList[0]

print(out := sort_algorithm([
	{
		"question_words": ["what"],
		"keywords": ["time"],
		"to_be": [],
		"intent": "inquire",
		"subject": "user",
		"assets": None,
		"references": {},
		"full_command": "what time is it",
		"command": "what time is it",
		"reply": "It's 02 33 PM",
		"audio_index": "000005",
		"from_cache": False
	},

	{
		"question_words": ["what"],
		"keywords": ["time"],
		"to_be": [],
		"intent": "inquire",
		"subject": "user",
		"assets": None,
		"references": {},
		"full_command": "what time is it",
		"command": "what time is it",
		"reply": "It's 02 32 PM",
		"audio_index": "000006",
		"from_cache": False
	},

	{
		"question_words": ["what"],
		"keywords": ["time"],
		"to_be": [],
		"intent": "state",
		"subject": "user",
		"assets": None,
		"references": {},
		"full_command": "what time is it",
		"command": "what time is it",
		"reply": "It's 02 32 PM",
		"audio_index": "000006",
		"from_cache": False
	}
]), type(out), f"\nReturned content dictionaries: {1 if (type(out) is dict) else len(out)}")

intents = list()

if out is list:
	for i, _ in enumerate(out):
		intents.append(out[i].get("intent"))

print(f"Intents returned: {intents}")
