#
# FILENAME: wizard.py | Quinton-VoiceAssistant
# DESCRIPTION: Quinton's setup wizard
# CREATED: 2020-10-16 @ 2:29 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

"""
	The Quinton-VoiceAssistant setup wizard.

	In the future, this will be replaced with a GUI setup wizard.
"""

import yaml

from typing import NoReturn
from pathlib import Path

from voiceassistant import VoiceAssistant

def setupWizard(va: VoiceAssistant) -> NoReturn:
	"""
		An interactive setup wizard to configure Quinton and set some of it's settings without editing
		the configuration file. Also serves as a greeter.
	"""

	# The line numbers where a specific YAML key-value pair is (for example, the user's name is
	# entered on line 42).
	#
	# NOTE: The line numbers eventually need to be used to subscript a list (which is zero-indexed), so
	# the values are subtracted by one before they're used.
	#
	# The dictionary is YAML key mapped to line number
	LINE_INDICES = {
		"username": 42,
		"units": 44,
		"clear_frequency": 93
	}

	CONFIG_PATH = Path("../data/config/config.yaml")

	fileLns = docs = list()

	with open(str(CONFIG_PATH), "r") as config:
		fileLns = config.readlines()

	# ------------------------------------------------------------------------------------------------------------------------

	# Get the user's name
	va.speak("Hello! My name is Quinton. What is your name?")

	(newPair := yaml.full_load(fileLns[LINE_INDICES.get("username") - 1])).update({"username": va.listen().title()})

	name = newPair.get('username')

	# Update the configuration value while preserving the line comment
	#
	# NOTE: Use `chr(10)` to get a "\n" while avoiding `SyntaxError: f-string expression part cannot include a backslash`
	fileLns[LINE_INDICES.get("username") - 1] = str()
	fileLns[LINE_INDICES.get("username") - 1] = f"{yaml.dump(newPair).strip(chr(10))} # Your name here\n"

	# ------------------------------------------------------------------------------------------------------------------------

	# Get the user's preferred units
	va.speak(f"Hello, {name}, nice to meet you! I have a few more questions to ask you. First, do you use " + \
			  "imperial or metric units?")

	(newPair := yaml.full_load(fileLns[LINE_INDICES.get("units") - 1])).update({"units": va.listen()})

	# Update the configuration value while preserving the line comment
	#
	# NOTE: Use `chr(10)` to get a "\n" while avoiding `SyntaxError: f-string expression part cannot include a backslash`
	fileLns[LINE_INDICES.get("clear_frequency") - 1] = str()
	fileLns[LINE_INDICES.get("clear_frequency") - 1] = f"{yaml.dump(newPair).strip(chr(10))} # \"imperial\" (default) or \"metric\""

	# ------------------------------------------------------------------------------------------------------------------------

	# Get the user's preferred frequency of clearing the cache
	va.speak("Finally, how often do you want the cache cleared? Please choose from daily, weekly, " + \
			 "monthly, anually, or never.")

	(newPair := yaml.full_load(fileLns[LINE_INDICES.get("clear_frequency") - 1])).update({"clear_frequency": va.listen()})

	# Update the configuration value while preserving the line comment
	#
	# NOTE: Use `chr(10)` to get a "\n" while avoiding `SyntaxError: f-string expression part cannot include a backslash`
	fileLns[LINE_INDICES.get("clear_frequency") - 1] = str()
	fileLns[LINE_INDICES.get("clear_frequency") - 1] = f"{yaml.dump(newPair).strip(chr(10))} # Select from: \"daily\", \"weekly\", \"monthly\", \"annually\" (default), or \"never\""

	# ------------------------------------------------------------------------------------------------------------------------

	with open(str(CONFIG_PATH), "w") as config:
		# Clear the file and reset the cursor
		config.truncate(0)
		config.seek(0)

		# Edit the configuration file
		config.writelines(fileLns)
