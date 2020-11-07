#
# FILENAME: cache.py | Quinton-VoiceAssistant
# DESCRIPTION: The Cache class for controlling Quinton's memory
# CREATED: 2020-06-03 @ 1:54 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Controls to directly modify Quinton's cache. """

import os, pytz
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
		self.clearFrequency = clearFrequency
		self.timezone = timezone
		print("Timezone:", self.timezone)

	# def getClearDate() -> str:
	# 	""" Get the date that the next cache clear happens on. """

	# 	MONTHS = 12
	# 	tz = pytz.timezone(self.timezone) # Get the timezone

	# 	# Get the current date
	# 	time = datetime.now(pytz.timezone(tz.zone))

	# 	dt = datetime.strptime((str(time.day) + "/" + str(time.month) + "/" + str(time.year) + " " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)), "%d/%m/%Y %H:%M:%S")
		
	# 	if self.clearFrequency == "daily":
	# 		# dt = datetime.strptime((str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)), "%I:%M:%S")
	# 		# fmt = "%I:%M:%S %p"

	# 		# time_now = dt.strftime(fmt)

	# 		return "12:00:00 AM"

		
	# 	month = time.month

		

	# 	# fmt = "%B %d" # Month and day (ex. January 01)
	# 	# date = dt.strftime(fmt)
	# 	# self.clearDate = (date.split()[0], int(date.split()[1])) # Split the month and day, and have the day as an integer (ex. ("January", 1))

	# 	# fmt = ""

	@staticmethod
	def __clear() -> bool:
		""" Clear Quinton's cache. Retruns true if there were no errors. """
		success1 = os.system("rm ../data/cache/responses/*") # Clear the audio recordings
		success2 = os.system("rm ../data/cache/history/*") # Clear the corresponding history files

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
				self.__updateLastClear(rfromForce=force)
			
			return couldClear 

		data = str()
		couldClear = False

		with open("../data/memory/last-cache-clear.txt") as lcc:
			data = lcc.read()
		
		if os.stat("../data/memory/last-cache-clear.txt").st_size != 0:
			print("Here")
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
			elif self.clearFrequency == "manually": # NOTE: Manual cache clearing isn't allowed in v0.1.0 
				couldClear = NotImplemented
		else:
			print("Else")
			couldClear = self.__clear
			print("Could clear:", couldClear)
		
		couldClear = False if couldClear is NotImplemented else couldClear

		if couldClear: 
			self.__updateLastClear(r)

		return couldClear
	
	# The following methods may be deprecated before the initial release. if they aren't, they
	# may end up being features only for the developer version.
	@staticmethod
	def checkFor(audioID: str) -> bool:
		from warnings import warn 
		warn(DeprecationWarning)

		try:
			# Check for a certain audio ID number in the cache
			matches = int(os.popen(f"ls ../data/cache/responses | grep -c {audioID}").read())
		except OSError:
			quit()
		finally:
			return (matches > 0)

	@staticmethod
	def get(audioID: str) -> Path:
		from warnings import warn 
		warn(DeprecationWarning)

		return Path("../data/cache/responses/" + audioID + ".wav")
