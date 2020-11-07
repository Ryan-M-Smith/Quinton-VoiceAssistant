# FILENAME: pathlibtest.py
# DESCRIPTION: A test using POSTIX paths instead of plain strings for file paths

from pathlib import Path
import json, os

filePath = Path("../data/cache/history")
filename = "history-000005.json"

with open(f"{filePath}/{filename}") as f:
	r = json.load(f)
	print(r, type(r))