#
# FILENAME: reader.py | Quinton-VoiceAssistant
# DESCRIPTION: Reads a Quinton ToolKit
# CREATED: 2020-11-21 @ 3:11 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Reads a Quinton ToolKit. """

import sys, os
from types import ModuleType
from typing import Generator
from importlib import import_module

sys.path.append(os.path.abspath(os.path.join("../"))) # Path is relative to `main.py`

# NOTE: Uncomment this once the code is verified to work. `exceptions` can't be imported
# from a direct run of this file.
from exceptions import ToolKitLoadError, ToolKitExistanceError

def checkRequirements(moduleName: str) -> bool:
	""" Checks to make sure the ToolKit has all of the required content. """

	module = import_module(moduleName)

	# NOTE: The `filter` call below this one obsoletes the following code
	classes = list(filter(lambda x: not x.startswith("_"), dir(module))) # Get rid of "__`x`__" (e.g. __name__)

	# Because all ToolKits must be prefixed with "TK", "TK_", or "TK-", the list of classes in
	# the ToolKit's file can be narrowed easily.
	#
	# There should never be more than one ToolKit in a file, so taking the first index
	# should be fine.
	className = list(filter(lambda c: c.startswith(("TK", "TK_", "TK-")), classes))[0]

	assert module is not None, ToolKitExistanceError.reason # Make sure everything checks out before using `eval`

	REQUIREMENTS = ["KEYWORDS", "CMPD_KEYWORDS", "ALT_KEYWORDS", "ASSETS"]

	for req in REQUIREMENTS:
		if hasattr(eval(f"module.{className}"), req):
			print("Yes")
		else:
			print("No")
			return False
	
	return True

def getContent(moduleName: str) -> list:
	"""
		Collect the data from the ToolKit's class. The class has already been confirmed to have
		all the required data by this point, so it's okay to go in and fetch it all.
	"""

	module = import_module(moduleName)

	REQUIREMENTS = ["KEYWORDS", "CMPD_KEYWORDS", "ALT_KEYWORDS", "ASSETS"]

	obj = eval("module.ToolKit") # Get the class

	# Use comprehension to collect the data as the requirements are iterated.
	return [getattr(obj, req) for req in REQUIREMENTS]

def require(moduleName: str) -> Generator[object, None, None]:
	""" Import a ToolKit. """

	module = import_module(moduleName)

	assert (module is not None) and (moduleName is not None) # This is unlikely to fail

	yield eval(f"module.{moduleName}")


checkRequirements("toolkit_template")
print(*getContent("toolkit_template"))