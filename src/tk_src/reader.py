#
# FILENAME: reader.py | Quinton-VoiceAssistant
# DESCRIPTION: Reads a Quinton ToolKit
# CREATED: 2020-11-21 @ 3:11 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

from types import ModuleType
from importlib import import_module

# NOTE: Temporary
class ToolKitExistanceError(Exception):
	""" A ToolKit failed the assertion test for `None`. """
	reason = "The ToolKit doesn't exist"
	code = 113

class ToolKitLoadError(Exception):
	""" There was a problem loading a toolkit. """

	reason: str
	code = 114

	def __init__(self, tkname: str):
		""" Allow the exception to take an argument. """
		self.reason = f"There was a problem loading the ToolKit {tkname}. Aborting."
	
	def __str__(self) -> str:
		return reason

# NOTE: Uncomment this once the code is verified to work. `exceptions` can't be imported
# from a direct run of this file.
#from exceptions import ToolKitLoadError, ToolKitExistanceError

def checkRequirements(moduleName: str, *, _module: ModuleType = None) -> bool:
	""" Checks to make sure the ToolKit has all of the required content. """

	module = import_module(moduleName)

	print(list(filter(lambda x: not x.startswith("_"), dir(module)))) # Get rid of "__`x`__" (e.g. __name__)

	assert module is not None, ToolKitExistanceError.reason # Make sure everything checks out before using `eval`

	REQUIREMENTS = ["KEYWORDS", "CMPD_KEYWORDS", "ALT_KEYWORDS", "ASSETS"]

	for req in REQUIREMENTS:
		if hasattr(eval("module.ToolKit"), req):
			print("Yes")


checkRequirements("toolkit_template")