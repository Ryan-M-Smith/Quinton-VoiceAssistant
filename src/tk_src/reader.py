#
# FILENAME: reader.py | Quinton-VoiceAssistant
# DESCRIPTION: Reads a Quinton ToolKit
# CREATED: 2020-11-21 @ 3:11 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

from types import ModuleType
from importlib import import_module

def checkRequirements(moduleName: str, *, _module: ModuleType = None) -> bool:
	""" Checks to make sure the ToolKit has all of the required content. """

	module = import_module(moduleName)

	print(list(filter(lambda x: not x.startswith("_"), dir(module)))) # Get rid of "dunder x dunder"

	assert module is not None # Make sure everything checks out before using `eval`

	if hasattr(eval("module.ToolKit"), "KEYWORDS"):
		print("Yes")


checkRequirements("toolkit_template")