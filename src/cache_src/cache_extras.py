#
# FILENAME: cache_extras.py | Quinton-VoiceAssistant
# DESCRIPTION: Unused functions that may still serve a purpose 
# CREATED: 2020-11-29 @ 3:30 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

""" Unused functions that may still serve a purpose. """

import os, subprocess
from pathlib import Path
from typing import Optional

def checkFor(audioID: str) -> bool:
	"""
		Check for a specific audio recording in the cache. The parameter can be the id with or without
		the file extension (in this case .wav).

		Example: `cache_extras.check("000001.wav")` and `cache_extras.check("000001")` give the same result.

		Return `True` if the file is found, `False` otherwise.
	"""

	matches = int()
	
	RESPONSE_PATH = Path(../data/cache/responses) # A path relative to `main.py`

	try:
		# Check for a certain audio ID number in the cache
		matches = int(subprocess.check_output(f"ls {RESPONSE_PATH} | grep -c {audioID}", shell=True).decode("utf-8"))
	except Exception: # Something went wrong
		quit()
	finally:
		return matches > 0

def get(audioID: str) -> Optional[Path]:
	"""
		Get the path of a particular audio recording from the cache.

		Return the path to the file (as a `pathlib.Path` object) if the file exists, otherwise return `None`.
	"""

	filepath = f"../../data/cache/responses/{audioID}.wav"

	return Path(filepath) if os.path.exists(Path(filepath)) else None

# NOTE: In case I end up including this code as a legitimate feature, I want to still
# have it so I can pick up where I left off.
def __getClearDate() -> str:
		"""
			Final functionality: Get the date that the next cache clear happens on.
			
			THIS FUNCTION IS INCOMPLETE AND DOES NOT WORK.
		"""

		MONTHS = 12
		#tz = pytz.timezone(self.timezone) # Get the timezone

		# Get the current date
		time = datetime.now() #pytz.timezone(tz.zone))

		dt = datetime.strptime((str(time.day) + "/" + str(time.month) + "/" + str(time.year) + " " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)), "%d/%m/%Y %H:%M:%S")
		
		if self.clearFrequency == "daily":
			# dt = datetime.strptime((str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)), "%I:%M:%S")
			# fmt = "%I:%M:%S %p"

			# time_now = dt.strftime(fmt)

			return "12:00:00 AM"

		
		month = time.month

		# fmt = "%B %d" # Month and day (ex. January 01)
		# date = dt.strftime(fmt)
		# self.clearDate = (date.split()[0], int(date.split()[1])) # Split the month and day, and have the day as an integer (ex. ("January", 1))

		# fmt = ""
