#
# FILENAME: main.py | Quinton-VoiceAssistant
# DESCRIPTION: The main file for the voice assistant
# CREATED: 2020-03-26 @ 2:25 PM
# COPYRIGHT: Copyright (c) 2020-2021 by Ryan Smith <rysmith2113@gmail.com>
#

""" Instantiate and run Quinton (with error handlers). """

import sys, warnings
from typing import NoReturn

from exceptions import Error, Warn, UnknownProblem, PyVersionError
from voiceassistant import VoiceAssistant

from config_src.config import Config
from config_src.permissions import Permissions as Perms

from cache_src.cache import Cache
from cache_src.history import History

import wizard, datalogging as dl

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
	try:
		cfg.setFromConfig(cfg)
	except (Exception, Warning, Error, Warn) as e: # Handle exceptions and warnings
		print(type(e))

		# Convert the type name of any warning to a common name
		# in the same format as the items in resulting list of `Warn.getSubclasses()`.
		e_common = str()

		if issubclass(type(e), (Warning, Warn)):
			e_common = str(type(e)).strip("<>").split()[1].strip("\'")

		if isinstance(e, Error): # Detect errors
			print("Error")
			dl.speak(e.reason, cfg=cfg)
			dl.log(error=e, reason=e.reason, code=e.code)
		elif e_common in (wscs := Warn.getSubclasses()).keys(): # Detect warnings
			# Because the check for warnings involves comparing the common names, there
			# is no callable class object. Instead, the corresponding dictionary value
			# (Warn subclass object) mapped to the common name is used to get the reason.
			print("Warning")
			dl.speak(text=getattr(wscs.get(e_common), "reason"), cfg=cfg)
			dl.log(
				error=wscs.get(e_common),
				reason=getattr(wscs.get(e_common), "reason"),
				code=getattr(wscs.get(e_common), "code")
			)
		else:
			print("Other Error")
			dl.speak(UnknownProblem.reason, cfg=cfg)
			dl.log(error=UnknownProblem, reason=UnknownProblem.reason, code=UnknownProblem.code)

		# Abort the program with the exit code of the specific exception that was raised
		if type(e) is not UserWarning:
			if (issubclass(type(e), Exception)) or (isinstance(e, Error)) or (type(e) is Exception):
				exit(e.code)

	# NOTE: The configuration is set up; error data is now spoken as well as logged

	# Python version check
	#
	# NOTE: The function portion may be removed later, but right now the block
	# has fairly good readability.
	if not versionCheck():
		raise PyVersionError

	# Get the user permissions
	try:
		perms.setPermsFromCfg(cfg)
		perms.getPerms()
	except (Exception, Warning, Error, Warn) as e: # Handle exceptions and warnings
		print(type(e))

		# Convert the type name of any warning to a common name
		# in the same format as the items in resulting list of `Warn.getSubclasses()`.

		e_common = str()

		if issubclass(type(e), (Warning, Warn)):
			e_common = str(type(e)).strip("<>").split()[1].strip("\'")

		if isinstance(e, Error): # Detect errors
			print("Error")
			dl.speak(e.reason, cfg=cfg)
			dl.log(error=e, reason=e.reason, code=e.code)
		elif e_common in (wscs := Warn.getSubclasses()).keys(): # Detect warnings
			# Because the check for warnings involves comparing the common names, there
			# is no callable class object. Instead, the corresponding dictionary value
			# (Warn subclass object) mapped to the common name is used to get the reason.
			print("Warning")
			dl.speak(text=getattr(wscs.get(e_common), "reason"), cfg=cfg)
			dl.log(
				error=wscs.get(e_common),
				reason=getattr(wscs.get(e_common), "reason"),
				code=getattr(wscs.get(e_common), "code")
			)
		else:
			print("Other Error")
			dl.speak(UnknownProblem.reason, cfg=cfg)
			dl.log(error=UnknownProblem, reason=UnknownProblem.reason, code=UnknownProblem.code)

		# Abort the program with the exit code of the specific exception that was raised
		if type(e) is not UserWarning:
			if (issubclass(type(e), Exception)) or (isinstance(e, Error)) or (type(e) is Exception):
				exit(e.code)

	# Create an instance of the `VoiceAssistant` class
	try:
		va = VoiceAssistant(cfg=cfg, perms=perms)
	except (Exception, Warning, Error, Warn) as e: # Handle exceptions and warnings
		print(type(e))

		# Convert the type name of any warning to a common name
		# in the same format as the items in resulting list of `Warn.getSubclasses()`.

		e_common = str()

		if issubclass(type(e), (Warning, Warn)):
			e_common = str(type(e)).strip("<>").split()[1].strip("\'")

		if isinstance(e, Error): # Detect errors
			print("Error")
			dl.speak(e.reason, cfg=cfg)
			dl.log(error=e, reason=e.reason, code=e.code)
		elif e_common in (wscs := Warn.getSubclasses()).keys(): # Detect warnings
			# Because the check for warnings involves comparing the common names, there
			# is no callable class object. Instead, the corresponding dictionary value
			# (Warn subclass object) mapped to the common name is used to get the reason.
			print("Warning")
			dl.speak(text=getattr(wscs.get(e_common), "reason"), cfg=cfg)
			dl.log(
				error=wscs.get(e_common),
				reason=getattr(wscs.get(e_common), "reason"),
				code=getattr(wscs.get(e_common), "code")
			)
		else:
			print("Other Error")
			dl.speak(UnknownProblem.reason, cfg=cfg)
			dl.log(error=UnknownProblem, reason=UnknownProblem.reason, code=UnknownProblem.code)

		# Abort the program with the exit code of the specific exception that was raised
		if type(e) is not UserWarning:
			if (issubclass(type(e), Exception)) or (isinstance(e, Error)) or (type(e) is Exception):
				exit(e.code)

	wizard.setupWizard(va)

	# Run the voice assistant
	try:
		print("Running")

		while True:
			va.run()
	except (Error, Warn) as e: # Handle exceptions and warnings
		print(type(e))

		# Convert the type name of any warning to a common name
		# in the same format as the items in resulting list of `Warn.getSubclasses()`.

		e_common = str()

		if issubclass(type(e), (Warning, Warn)):
			e_common = str(type(e)).strip("<>").split()[1].strip("\'")

		print("e_common: ", e_common)

		if isinstance(e, Error): # Detect errors
			print("Error")
			dl.speak(e.reason, cfg=cfg)
			dl.log(error=e, reason=e.reason, code=e.code)
		elif e_common in (wscs := Warn.getSubclasses()).keys(): # Detect warnings
			# Because the check for warnings involves comparing the common names, there
			# is no callable class object. Instead, the corresponding dictionary value
			# (Warn subclass object) mapped to the common name is used to get the reason.
			print("Warning")
			dl.speak(text=getattr(wscs.get(e_common), "reason"), cfg=cfg)
			dl.log(
				error=wscs.get(e_common),
				reason=getattr(wscs.get(e_common), "reason"),
				code=getattr(wscs.get(e_common), "code")
			)
		else:
			print("Other Error")
			dl.speak(UnknownProblem.reason, cfg=cfg)
			dl.log(error=UnknownProblem, reason=UnknownProblem.reason, code=UnknownProblem.code)

		# Abort the program with the exit code of the specific exception that was raised
		if type(e) is not UserWarning:
			if (issubclass(type(e), Exception)) or (isinstance(e, Error)) or (type(e) is Exception):
				exit(e.code) #if isinstance(e, Error) else None)

if __name__ == "__main__":
	sys.exit(main())
