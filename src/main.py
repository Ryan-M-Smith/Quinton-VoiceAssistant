#
# FILENAME: main.py | Quinton-VoiceAssistant
# DESCRIPTION: The main file for the voice assistant
# CREATED: 2020-03-26 @ 2:25 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

""" Instantiate and run Quinton (with error handlers). """

import sys, warnings
from typing import NoReturn

from .exceptions import Error, Warn, UnknownProblem, PyVersionError
from .voiceassistant import VoiceAssistant

from .config_src.config import Config
from .config_src.permissions import Permissions as Perms

from .cache_src.cache import Cache
from .cache_src.history import History

from . import wizard
from .handler import handle

def versionCheck() -> bool:
	""" Make sure the user is using a compatible version of Python (v3.8.0+). """
	return (sys.version_info.major >= 3) and (sys.version_info.minor >= 8)

def main() -> NoReturn:
	""" Run everyhting and control the exception handler. """

	warnings.filterwarnings("error") # Allow warnings to be caught by a try-except block
	warnings.formatwarning(message=None, category=Warn, filename="voiceassistant.py", lineno=0, line=None) # Formating for all warnings

	cfg = Config()
	perms = Perms()

	# Call all of the functions required to run Quinton, starting with the configuration functions.
	# These are the functions that set everything up before an instance of the `VoiceAssistant` class
	# can be created.

	# Load the configuration first so error feedback can be spoken starting at the next handler.
	# Because there is no existing configuration to pass to the `datalogging.speak()` function,
	# any errors here are silently logged.
	handle(cfg.setFromConfig, cfg, cfg=cfg)

	# NOTE: The configuration is set up; error data is now spoken as well as logged

	# Python version check
	#
	# NOTE: The function portion may be removed later, but right now the block
	# has fairly good readability.
	if not versionCheck():
		raise PyVersionError

	# Get the user permissions
	handle(perms.setPermsFromCfg, cfg, cfg=cfg)
	handle(perms.getPerms, cfg=cfg)

	# Create an instance of the `VoiceAssistant` class
	va = handle(VoiceAssistant, cfg, perms, cfg=cfg)

	wizard.setupWizard(va)

	# Run the voice assistant
	while True:
		print("Running")
		handle(va.run, cfg=cfg)

if __name__ == "__main__":
	sys.exit(main())
