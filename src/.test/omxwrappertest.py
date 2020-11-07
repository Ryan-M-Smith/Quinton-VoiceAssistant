# FILENAME: omxwrappertest.py
# DESCRIPTION: A test using the omxplayer-wrapper python library

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from getpass import getuser
from tinytag import TinyTag

USER = getuser() # Get the name of the user currently logged in

AUDIO_PATH = Path("/home/" + USER + "/hello.wav")

audiolen = TinyTag.get(AUDIO_PATH).duration
print(audiolen)

player = OMXPlayer(AUDIO_PATH)

try:
    sleep(audiolen + 0.3) # Allow the audio to finish playing before quitting, and add a little leeway
except KeyboardInterrupt:
    print("\nAborted.")
    quit()
finally:
    player.quit() # Exit the player

