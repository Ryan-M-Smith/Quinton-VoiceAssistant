# FILENAME: setup.py
# Quinton-VoiceAssistant's build script

import setuptools

with open("README.md", "r") as ld, open("requirements.txt", "r") as req:
	long_description = ld.read()
	requirements = req.read().split("\n")

with open("version.txt", "r") as v:
	version = list(v.read().split("\n"))[0][9:] # Read the version line (first line) only

AUTHOR, EMAIL = "Ryan Smith", "rysmith2113@gmail.com"

setuptools.setup(
	name="Quinton-VoiceAssistant",
	version="0.1.1",
	author=AUTHOR,
	author_email=EMAIL,
	maintainer=AUTHOR,
	maintainer_email=EMAIL,
	description="A voice assistant",
	long_description=long_description, # The README
	long_description_content_type="text/markdown",
	url="https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant",
	packages=setuptools.find_packages(),
	license='GNU GPLv3+',
	platforms=["MacOS", "Linux"],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Topic :: Home Automation",
		"Programming language :: Python :: 3 :: Only"
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSTIX :: Linux",
		"Environment :: Console",
	],
	install_requires=requirements,
	python_requires=">=3.8",
	package_data={
		"data": ["data/"],
		"doc": ["doc/"]
	},
	include_package_data=True,
	entry_points={"console_scripts": ["main=src.main:main"]}
)