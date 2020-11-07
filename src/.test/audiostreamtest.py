# FILENAME: audiostreamtest.py
# A test with audio streaming using the PyAudio Python library

import pyaudio, wave, time
from omxplayer.player import OMXPlayer
from tinytag import TinyTag

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
OUTPUT = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	frames_per_buffer=CHUNK
)

print("Recording...")

frames = list()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)

print("Done!")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(OUTPUT, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()

audiolen = TinyTag.get(OUTPUT).duration
print(audiolen)

player = OMXPlayer(OUTPUT)

try:
    time.sleep(audiolen + 0.3) # Allow the audio to finish playing before quitting, and add a little leeway
except KeyboardInterrupt:
    print("\nAborted.")
    quit()
finally:
    player.quit() # Exit the player

print(TinyTag.get(OUTPUT).audio_offset, TinyTag.get(OUTPUT).bitrate)
