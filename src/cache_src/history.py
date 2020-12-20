#
# FILENAME: history.py | Quinton-VoiceAssistant
# DESCRIPTION: The history class for accessing command history
# CREATED: 2020-06-09 @ 4:25 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" A "read-only" cache controller which allows the cache to be searched for data. """

import json, os, subprocess
from pathlib import Path

# NOTE: This class has one static method. Using a class here is probably unnecessary and this module
# will likely only contain the function in the future.
class History:
	""" 
		The history class adds cache searching functionality. This helps the Cache object
		find the correct audio file to play back to the user when using a cached answer.
	"""

	@staticmethod
	def search(command: str) -> (bool, list, list):
		""" 
			Search for a command in the history. Return whether or not the command was found, and
			a list of the audio indices of audio files with responses to the command. This way,
			the response to the command can still be random, just like if it was newly generated. 
		"""

		filelen = int()

		# Define some paths
		HIST_PATH = Path("../data/cache/history")
		LSOUT_PATH = Path("../data/tmp/lsout.txt")

		try:
			# Save the result of running `ls ../data/cache/responses` to `../data/tmp/lsout.txt`.
			contents = subprocess.check_output(f"ls {HIST_PATH} &> {LSOUT_PATH}", shell=True).decode("utf-8")

			# Write the contents to `../data/tmp/lsout.txt`
			with open(LSOUT_PATH, "w") as lsout:
				lsout.write(contents)

			# Get the number of files in the `../data/cache/history` directory. Newlines are not stripped here because 
			# `wc -l` checks for newline characters to calculate line number. The character count in the file is also stored
			# to check for potential file lengths of 1 without an empty second line.
			filelen = int(subprocess.check_output(f"cat -A {LSOUT_PATH} | wc -l", shell=True).decode("utf-8"))
			charCount = int(subprocess.check_output(f"cat -A {LSOUT_PATH} | wc -c", shell=True).decode("utf-8").strip("\n"))
		except OSError:
			quit()
		finally:
			# Check if the file is empty or if a lack of newline characters causes 
			# #`wc -l` to return `0`
			if filelen == 0:
				if charCount > 0:
					filelen = 1
				else:
					filelen = None
		
		# Will be returned in a tuple
		idList = list()
		dataList = list()
		foundMatchingCmd = False

		if filelen is not None:
			files = list()

			for i in range(0, filelen):
				# Read the file line by line while stripping trailing newlines
				files.append(subprocess.check_output(f"less ../data/tmp/lsout.txt | sed -n \'{i + 1}p\'", shell=True).decode("utf-8").strip("\n"))

			if files[-1] == "":
				files.__delitem__(-1) # Remove a trailing newline at the end of the output file
			
			# Check for a certain command in every file. If it's found, save the audio index
			for _, hfile in enumerate(files):
				# Skip over files that are empty
				if os.stat(f"{HIST_PATH}/{hfile}").st_size != 0:
					with open(f"{HIST_PATH}/{hfile}") as h:
						hdict = json.load(h) # Convert the JSON in the file to a Python dictionary

						# Check for the command
						if hdict.get("command") == command:
							if not foundMatchingCmd:
								foundMatchingCmd = True

							idList.append(hdict.get("audio_index"))
							dataList.append(hdict)
				else:
					subprocess.call(f"rm {HIST_PATH}/{hfile}", shell=True)
		
		if not foundMatchingCmd:
			idList = dataList = None
		
		return (foundMatchingCmd, idList, dataList)
