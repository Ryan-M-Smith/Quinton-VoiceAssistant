# FILENAME: tzcodes.py
# A helper script which lists valid pytz timezone names for Quinton to use.
#
# This script is an automated, more user-friendly adaptation of timezone list search 
# methods from the pytz README (github.com/stub42/pytz/blob/master/src/README.rst).
#

from pytz import all_timezones, common_timezones

# Allow the user to use the list of common timezones
common = input("Would you like to use pytz's list of common timezones (yes/no)? ")
USE_COMMON = True if common.lower().strip() == "yes" else False

country = input("Enter the name of your country (type \"America\" for United States): ")

foundtz = bool()

# Filter and print out timezones for the specified country. Any characters in the `country`
# variable are matched ONLY to the country names in a timezone list (i.e., before the "/").
#
# Example: The characters "ame" are entered. This matches to "America/Eastern", but not "Africa/Ndjamena",
# because the "ame" doesn't occur in the country name.
#
for timezone in (common_timezones if USE_COMMON else all_timezones):
	if (country.lower().strip() in (tzl := timezone.lower())[:tzl.find("/")]) or (country.strip() == str()):
		if not foundtz:
			foundtz = True
		
		print(timezone)

# No results found
if not foundtz:
	print("No results matched your search.")