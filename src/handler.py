#
# FILENAME: handler.py | Quinton-VoiceAssistant
# DESCRIPTION: The exception handler for the voice assistant
# CREATED: 2021-06-04 @ 8:04 PM
# COPYRIGHT: Copyright (c) 2021 by Ryan Smith <rysmith2113@gmail.com>
#

from typing import Any, Callable

from . import datalogging as dl
from .config_src.config import Config
from .exceptions import Error, Warn, UnknownProblem

def handle(process: Callable[..., Any], *args, cfg: Config) -> Any:
	"""
		The Quinton-VoiceAssistant exception handler

		Call `process()` under the `try` clause of a large `try`-`except` block.
	"""
	try:
		return process(*args) # Call the function with the correct arguments
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