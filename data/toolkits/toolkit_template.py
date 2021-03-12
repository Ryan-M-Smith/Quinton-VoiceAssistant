#
# FILENAME: toolkit_template.py | Quinton-VoiceAssistant
# DESCRIPTION: A sample ToolKit
# CREATED: 2020-11-21 @ 3:37 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

import sys
from typing import Union, Optional # If you want to remove type annotations, you don't need these

class TK_ToolKit:
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

	KEYWORDS = [
		"hello"
	]

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

	def reply(self, commandInfo: Union[dict, list]) -> (str, dict):
		""" Reply to the command based on predefined test cases. """

		TEST_CASES = [
			bool("hello" in commandInfo.get("keywords"))
		]

		print(TEST_CASES)

		for i, case in enumerate(TEST_CASES):
			print(case)
			if case:
				return (self.__results(i), commandInfo)


	@staticmethod
	def __results(casenum: int) -> str:
		"""
			The results of each specific case. The result numbers should match with the order of
			the cases in `TEST_CASES` (in `self.reply`).

			Example: `TEST_CASES[0]` should go with result 0.
		"""

		response = str()

		if casenum == 0:
			response = "The ToolKit works!"

		return response
