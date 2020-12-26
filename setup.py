# FILENAME: setup.py
# Quinton-VoiceAssistant's setup script

import setuptools, subprocess, os, sys
from distutils.cmd import Command
from setuptools.command.install import install

class PkgInstall(Command):
	""" 
		Defines a custom `pkginstall` command as well as a `--pkg-install` (`-k`) argument
		for the `setup.py` script. 
	"""

	description = "Install dependencies from the system package manager"
	user_options = [
		#("pkg-install", "k", description),	# Default `True`
		("pkg-install=", "k", description)	# Specify `True` or `False`
	]

	pkg_install: bool # This type is seemingly enforced

	def initialize_options(self):
		""" Set default values for the options. """
		self.pkg_install = True
	
	def finalize_options(self):
		""" Post-process options. """

		# When the user passes in a value (either `True` or `False`), it is read in
		# as a string. To use it as a boolean, it must be put through `eval`.
		if eval(str(self.pkg_install)):
			# Make sure the install script is executable. In order to achieve the same
			# result as running `chmod 755 dep-manager.sh`, an octal number must be used
			# rather than a base-10 integer for the mode.
			os.chmod("dep-manager.sh", mode=0o755)
	
	def run(self):
		""" Run the functionality. """

		if eval(str(self.pkg_install)):
			self.announce("Installing dependencies from the system package manager")
			subprocess.call(f"{os.environ.get('SHELL')} dep-manager.sh install", shell=True)

class CompleteInstall(install, PkgInstall):
	""" 
		A complete installation command for Quinton-VoiceAssistant, including the functionality
		to install non-Python dependencies.
	"""

	user_options = install.user_options + PkgInstall.user_options
	print(user_options)

	pkg_install = True if ("--pkg-install", "-k") in sys.argv else False # See if the user is using the argument

	def initialize_options(self):
		""" Set default values for the options. """
			
		if self.pkg_install:
			PkgInstall.initialize_options()
		
		install.initialize_options(self)
	
	def finalize_options(self):
		""" Post-process options. """

		if self.pkg_install:
			PkgInstall.finalize_options()
		
		install.finalize_options(self)

	def run(self):
		""" Run the `PkgInstall` functionality as well as the parent class's. """

		self.run_command("pkg_install")
		PkgInstall.run()
		install.run()

# Get the software's `pip` requirements
with open("README.md", "r") as ld, open("requirements.txt", "r") as req:
	long_description = ld.read()
	requirements = req.read().split("\n")
	

with open("version.txt", "r") as v:
	version = list(v.read().split("\n"))[0][9:] # Read the version line (first line) only

AUTHOR, EMAIL = "Ryan Smith", "rysmith2113@gmail.com"

setuptools.setup(
	cmdclass={
		"pkg_install": PkgInstall, 	# Only install non-Python dependencies (not the software)
		"install": CompleteInstall,	# Install everything (including non-Python dependencies)
		"orig_install": install 	# The default `install` functionality
	},

	name="Quinton-VoiceAssistant",
	version=version,
	author=AUTHOR,
	author_email=EMAIL,
	maintainer=AUTHOR,
	maintainer_email=EMAIL,
	description="A voice assistant",
	long_description=long_description, # The README
	long_description_content_type="text/markdown",
	url="https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant",
	
	# This web address directly downloads a zip archive of the project's master branch from GitHub.
	# If you want more download options or wish to clone the repository, see the `url` parameter
	# above or use `python3.9 setup.py --url`.
	download_url="https://www.github.com/Ryan-M-Smith/Quinton-VoiceAssistant/archive/master.zip",
	
	packages=setuptools.find_packages(),
	license='GNU GPLv3+',
	platforms=["MacOS", "Linux"],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Topic :: Home Automation",
		"Programming language :: Python :: 3 :: Only",
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
