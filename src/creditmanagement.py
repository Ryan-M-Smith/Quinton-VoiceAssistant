#
# FILENAME: creditmanagement.py | Quinton-VoiceAssistant
# DESCRIPTION: Code that fetches and updates the user's Houndify credit usage
# CREATED: 2021-06-07 @ 5:35 PM
# COPYRIGHT: Copyright (c) 2021 by Ryan Smith <rysmith2113@gmail.com>
#

import requests
from requests.auth import HTTPBasicAuth
from typing import Tuple
from bs4 import BeautifulSoup

DAILY_CREDITS = 100 # The number of Houndify credits allotted per day
used_credits = float()

# The baseline number of credits required for the Houndify domains that a client is
# registered under. Because Quinton is only registered under Speech-to-Text, and this
# domain requires no credits, the value is 0.
DOMAIN_CREDITS = 0

CPS = 0.25 # For all audio queries, Houndify uses 0.25 credits per second of audio

# Houndify username and password
USERNAME: str
PASSWORD: str

DASHBOARD_ID: str # The ID at the end of the Houndify dahsbord URL (https://www.houndify.com/dashboard/detail/[ID])

def getCredits() -> float:
		"""
			Use `BeautifulSoup` to fetch the currently used amount of Houndify credits from
			a user's account page.

			The Houndify API doesn't currently offer a way to do this, so I had to create
			a solution to this problem myself. If the API offers this functionality in the
			future, I'll depricate this functionality an use the official API.
		"""

		DASHBOARD_ID = "869d8cae-f7d5-42c2-a827-113f50173c8a"
		USERNAME, PASSWORD = "rysmith2113@gmail.com", "VoiceAssistantsRule"
		request = requests.get(f"https://www.houndify.com/dashboard/detail/{DASHBOARD_ID}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
		html = BeautifulSoup(request.text, "html.parser")
		print(html)

		# Use list comprehension to filter out HTML tags that don't contain the credit usage data.
		# if everything works properly, the resulting list should only have 1 element.
		tag = [str(s) for s in list(html.find_all("p")) if "usage-circle-value" in str(s)]
		print(len(tag))
		tag = tag[0] # Extract the HTML tag

		print(tag)

		#self.used_credits += float((self.CPS * (commandLen + wakeWord)) + self.DOMAIN_CREDITS)


def __creditsRemaining() -> Tuple[float, float]:
	"""
		Get the amount of Houndify credits used so far, and the amount remaining for
		the day.
	"""

	remaining = DAILY_CREDITS - used_credits
	return (used_credits, remaining)