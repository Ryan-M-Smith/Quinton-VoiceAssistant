#
# FILENAME: toolkit_template.py | Quinton-VoiceAssistant
# DESCRIPTION: A sample ToolKit
# CREATED: 2020-11-21 @ 3:37 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

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