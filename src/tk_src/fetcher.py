#
# FILENAME: fetcher.py | Quinton-VoiceAssistant
# DESCRIPTION: Collects ToolKit files from the source tree.
# CREATED: 2020-11-23 @ 11:09 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Collect ToolKits from the filesystem. """

import subprocess
from pathlib import Path
from importlib import import_module

def fetch() -> list:
	""" Collect all non-blacklisted ToolKits. """
	# For more info on blacklisting ToolKits, see `../doc/excluding-toolkits.md`.

	# Get a list of all the installed ToolKits. Filter out any files that start with an underscore (like `__init__.py`)
	# or a hidden file (like `.file.py`).
	filtered = filter(lambda tk: not tk.startswith(("_", ".")), subprocess.check_output("ls ../data/toolkits", shell=True).decode("utf-8").strip().split("\n"))
	TK_LIST = [tk for tk in filtered]

	EXCLUDE_FILE = Path("../data/config/toolkit-exclude.txt") # The list of ToolKits to exclude

	toolkits = list()

	with open(str(EXCLUDE_FILE), "r") as blacklist:
		for tk in TK_LIST:
			if not tk in blacklist.read().split("\n"):
				toolkits.append(f"data.toolkits.{tk.strip('.py')}")
	
	return toolkits
