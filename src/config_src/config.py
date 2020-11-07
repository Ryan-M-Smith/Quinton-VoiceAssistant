#
# FILENAME: config.py | Quinton-VoiceAssistant
# DESCRIPTION: The Config class
# CREATED: 2020-05-22 @ 4:53 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" 
	Contains functionality to set up Quinton prior to listening for commands. This includes:
		* Reading Quinton's YAML configuration file into Python
		* Determining if Quinton's weather info is correct
		* Loading portions of Quinton's memory
"""

import yaml, os, subprocess

from exceptions import (
	ConfigFileWarning,
	DefaultConfigError,
	CountryCodeError
)

class Config:
	""" Holds variables with info about Quinton and its settings. """

	# Less for use of the voice assistant and more for humans, although 
	# self.resetToDefault() uses one of them.
	CONFIG_PATH = "../data/config/config.yaml"
	DEFAULT_CFG_PATH = "../data/config/config.default.yaml"

	CLEAR_FREQUENCIES = [
		"daily",
		"weekly",
		"monthly",
		"anually", # Default
		"never",
		"manually"
	]

	# The variables to set from Quinton's configuration file
	username = str()
	wake_word = str()
	timezone = str()
	use_location: bool
	city = str()
	country = str()
	units = str()
	timeout: int
	time_limit: int
	ww_detect_time: int
	speaker_vol: int
	mic_vol: int
	pause: float
	
	log_data: bool
	clear_frequency = str()
	archive_audio_commands: bool
	record_command_history: bool
	timestamp_history: bool # Put a timestamp on recorded history
	#allow_usage_monitoring: bool# Unused in v0.1.0

	# Quinton's Espeak settings
	voice = str()
	speed: int
	pitch: int

	# The number of recorded responses stored in Quinton. 
	recordings = int()

	#
	# Custom configuration variables also go here. To learn more about custom config
	# variables, please read `../doc/custom-config.txt`.
	#

	@classmethod
	def setFromConfig(cls, self, /, yamlfile="../data/config/config.yaml"):
		""" 
			Read Quinton's configuration file and set the variables. By default, the main configuration
			file is used, but yamlfile can be changed to the path of the default configuration to reset
			Quinton.
		"""

		# Open and read Quinton's config file
		try:
			with open(yamlfile, mode="r") as configfile:
				config = list()
				
				# Load the YAML documents
				for doc in yaml.full_load_all(configfile):
					config.append(dict(doc))

				# Iterate through the documents and set the class variables from them. The variables are
				# set using setattr() for more concise code. For more information on this process, see
				# `../doc/reading-config.md`.

				# Max layers of nesting: 2 (The main layer doesn't count)
				for docnum in range(len(config)):
					for key, value in config[docnum].items(): # Iterate through all YAML documents in the file
						if type(value) is dict: # Handle nested dictionaries
							for l1_key, l1_value in value.items(): # Iterate through the nested dictionary
								if type(l1_value) is dict: # Check for another layer of nesting
									for l2_key, l2_value in l1_value.items(): # Iterate again
										setattr(cls, l2_key, l2_value)
								else:
									setattr(cls, l1_key, l1_value)
						else:
							setattr(cls, key, value)
		except FileNotFoundError:
			if yamlfile == self.DEFAULT_CFG_PATH:
				raise DefaultConfigError
			else:
				raise ConfigFileWarning
		else:
			# Set the amount of recordings already existing so the generator knows where to start.
			self.recordings = self.__getLastIndex()
			
			if self.recordings is None:
				self.recordings = 0

			if not (self.clear_frequency in self.CLEAR_FREQUENCIES):
				self.clear_frequency = "anually"
			
			# Check if the country code in Quinton's config meets OpenWeatherMap's requirements.
			meets = self.meets()
			if not meets:
				raise CountryCodeError

	@classmethod
	def resetToDefault(cls, self):
		""" Reset (or in some cases set) all configuration variables to default. """
		yamlfile = self.DEFAULT_CFG_PATH
		self.setFromConfig(cls, yamlfile)
	
	@staticmethod
	def __getLastIndex() -> int:
		""" 
			Get the current number of audio files saved in `../data/responses` to
			find a starting point for index generation. This functionality is only
			used upon a startup or reboot, because the generator creating the indexes
			can keep track as it works.
		"""

		amount = int()

		try:
			print("In try block...")
			
			# Save the result of running `ls ../data/cache/responses` to `../data/tmp/lsout.txt`
			contents = subprocess.check_output("ls ../data/cache/responses &> ../data/tmp/lsout.txt", shell=True).decode("utf-8") 

			# Write the contents to `../data/tmp/lsout.txt`
			with open("../data/tmp/lsout.txt", "w") as lsout:
				print("Writing contents...")
				lsout.write(contents)

			amount = int(subprocess.check_output("cat -A ../data/tmp/lsout.txt | wc -l", shell=True).decode("utf-8")) # Get the amount of recordings
		except OSError:
			quit()
		finally:
			if amount == int(): # amount is empty
				amount = None

			return amount
	
	def meets(self) -> bool:
		""" Determine if the country code in Quinton's config meets OpenWeatherMap's requirements. """
		# The code must be a two-character, uppercase string
		if (type(self.country) == str) and (len(self.country) == 2) and (self.country.isupper()):
			return True
		else:
			return False

# cfg = Config()
# cfg.setFromConfig(cfg)
# print(cfg.meets())
		