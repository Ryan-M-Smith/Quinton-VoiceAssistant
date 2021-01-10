#
# FILENAME: cache.py | Quinton-VoiceAssistant
# DESCRIPTION: The Cache class for controlling Quinton's memory
# CREATED: 2020-06-03 @ 1:54 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

""" Controls to directly modify Quinton's cache. """

import os, pytz, re, subprocess
from datetime import datetime
from pathlib import Path

class Cache:
	""" 
		Controls Quinton's memory. The cache class controls memory management and access to allow
		command replies to be generated faster.
	"""

	clearDate: tuple
	clearFrequency = str()
	timezone = str()

	def __init__(self, clearFrequency: str, timezone: str):
		"""
			The `Cache` class' constructor. Pass in the user-defined cache clear frequency
			and the set timezone for use with the time and date of the last cache clear.
		"""

		self.clearFrequency = clearFrequency
		self.timezone = timezone
		print("Timezone:", self.timezone)

	@staticmethod
	def __clear() -> bool:
		""" Clear Quinton's cache. Retruns true if there were no errors. """
		success1 = subprocess.check_output("rm ../data/cache/responses/*", shell=True) # Clear the audio recordings
		success2 = subprocess.check_output("rm ../data/cache/history/*", shell=True) # Clear the corresponding history files

		if (success1 == 0) and (success2 == 0):
			return True 
		else:
			return False
	
	def __updateLastClear(self, fromForce=False):
		""" 
			Update `../data/memory/last-cache-clear.txt` with the date of the most recent
			cache clear.
		"""
		tz = pytz.timezone(self.timezone) # Get the timezone
		time = datetime.now(pytz.timezone(tz.zone))

		fmt = "%d %m %Y %p"

		with open("../data/memory/last-cache-clear.txt", "w") as lcc:
			if fromForce:
				lcc.write(f"{time.strftime(fmt)} - Forced by user")
			else:
				lcc.write(time.strftime(fmt))

	def tryClear(self, force=False) -> bool:
		""" 
			Check if the cache should be cleared. If it should be, clear it. Returns
			`True` if the cache successfully cleared, `False` otherwise.
		"""

		if force:
			couldClear = self.__clear
			
			if couldClear:
				self.__updateLastClear(fromForce=force)
			
			return couldClear 

		data = str()
		couldClear = False

		with open("../data/memory/last-cache-clear.txt") as lcc:
			data = lcc.read()
		
		if os.stat("../data/memory/last-cache-clear.txt").st_size != 0:
			data = data.split()

			# Data is always in the form "dd mm yyyy AM/PM"
			last_clear_date = int(data[0])
			last_clear_month = int(data[1])
			last_clear_year = int(data[2])
			last_clear_tod = data[3] # Time of day (AM or PM)

			tz = pytz.timezone(self.timezone) # Get the timezone
			time = datetime.now(pytz.timezone(tz.zone))

			# Check certain scenarios to try to clear the cache.
			if self.clearFrequency == "daily":
				date = time.strftime("%d")

				if int(date) > last_clear_date:
					couldClear = self.__clear
			elif self.clearFrequency == "weekly":
				weekday = time.strftime("%w")

				# Clears every Sunday
				if int(weekday) == 0:
					couldClear = self.__clear
			elif self.clearFrequency == "monthly":
				month = time.strftime("%M")
				date = time.strftime("%d")

				# Clears on the 1st of every month
				if (int(month) > last_clear_month) and (int(date) == 1):
					couldClear = self.__clear
			elif self.clearFrequency == "annually":
				year = time.strftime("%Y")

				if int(year) > last_clear_year:
					couldClear = self.__clear
			elif self.clearFrequency == "never":
				# The cache will never be cleared, but this clause is still here to have
				# an exhaustive list of options. The `pass` statement effectively means
				# nothing will happen.
				pass
			elif self.clearFrequency == "manually": # NOTE: Manual cache clearing isn't currently allowed
				couldClear = NotImplemented
		else:
			couldClear = self.__clear
		
		couldClear = False if couldClear is NotImplemented else couldClear

		if couldClear: 
			self.__updateLastClear(r)

		return couldClear

	@staticmethod
	def clean() -> int:
		""" Clean the cache from garbage files (like a `None.wav` file when something goes wrong). """
		COMP = "[0-9][0-9][0-9][0-9][0-9][0-9]" # A 6-digit audio index

		CACHE_PATH = Path("../data/cache/responses")

		# NOTE: `str.partition()` could be used here, but `os`is already being used above.
		# Syntax: `f.partition(".")[0]`
		contents = [str(os.path.splitext(f)[0]) for f in subprocess.check_output(f"ls {str(CACHE_PATH)}", shell=True).decode("utf-8").strip().split("\n")]

		# Compare the file names to the compiled pattern
		for f in contents:
			if not (pattern := re.compile(COMP)).fullmatch(f):
				subprocess.call(f"rm {str(CACHE_PATH)}/{f}*", shell=True)