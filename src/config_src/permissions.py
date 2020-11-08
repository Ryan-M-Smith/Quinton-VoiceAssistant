#
# FILENAME: permissions.py | Quinton-VoiceAssistant
# DESCRIPTION: Quinton's permissions, used by other classes to limit/allow certain functionality based on the user's config 
# CREATED: 2020-08-09 @ 4:42 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

""" Formally define what the user allows (and doesn't allow) Quinton to do. """

from typing import NoReturn

from .config import Config

# NOTE: In the futre, this class may be turned into a module with two functions
class Permissions:
	""" Holds Quinton's permission settings and the methods that set them. """

	# All will be false by default
	canLogData = False
	canUseLocation = False
	canClearCache = False
	canSaveToCache = False
	canMonUsage = False
	canTimestampHist = False

	def setPermsFromCfg(self, cfg: Config) -> NoReturn:
		""" Set Quinton's permission variables from an instance of Config().  """

		if cfg.use_location:
			self.canUseLocation = True
		
		if cfg.log_data: # If data logging is on, everything is allowed
			self.canLogData = self.canClearCache = \
			self.canSaveToCache = self.canMonUsage = \
			self.canTimestampHist = True
		elif cfg.log_data == "custom":
			# Determine if the cache can be cleared from a custom data setting. A decision
			# would be made based on whether or not the user allows BOTH of the cache control
			# variables. Even if these are both allowed, a user may opt to never have their cache
			# cleared. 
			if (not cfg.record_command_history) or (not cfg.archive_audio_commands):
				# All cache usage is turned off
				self.canSaveToCache = self.canClearCache = self.canTimestampHist = False
			else:
				# Cache saving can happen (but not necessarily clearing or history timestamping)
				self.canSaveToCache = True

			# Check for the user specifically turning off cache clearing
			if cfg.clear_frequency != "never":
				self.canClearCache = True
			
			# Check if the user wants history entries timestamped
			if cfg.timestamp_history:
				self.canTimestampHist = True
		else:
			self.canLogData = self.canClearCache = \
			self.canSaveToCache = self.canMonUsage = \
			self.canTimestampHist = False

	def getPerms(self) -> list:
		return [
			self.canLogData,
			self.canMonUsage,
			self.canSaveToCache,
			self.canClearCache,
			self.canTimestampHist,
			self.canUseLocation
		]
