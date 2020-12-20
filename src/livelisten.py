#
# FILENAME: livelisten.py | Quinton-VoiceAssistant
# DESCRIPTION: Records live audio and gets its intensity to determine if it could possibly be speech. 
# CREATED: 2020-08-19 @ 4:38 PM
# COPYRIGHT: Copyright (c) 2020 by Ryan Smith <rysmith2113@gmail.com>
#

"""
	Records live audio and gets its intensity to determine if it could possibly be speech. This way,
	Houndify credits aren't wasted on empty requests (silence) or noise without speech (like a lawn
	mower running).
"""

import subprocess, math, wave
from alsaaudio import Mixer
from pyaudio import PyAudio, paInt16, Stream
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from time import sleep

from config_src.config import Config

# NOTE: This file may be converted to a file of functions rather than a class in the future
class Listener:
	"""
		The `Listener` class records audio, then compares the decibel value of the audio against
		a range of decibel values for normal speech (50-70 dB) to see if the speech is worth sending
		to Houndify for TTS or not.
	"""

	# The minimum pressure threshold in Pascals, effectively representing 0 dB. Note that
	# The actual decibel value of this number is somewhere around 4 dB, but it is most
	# commonly used as a reference point of 0 dB.
	__PRESSURE_TSHLD = float(2 * math.pow(10, -5))

	alsaMixer = Mixer(control="Capture") # Used to control recording volume

	recordLen: int

	def __init__(self, cfg: Config):
		""" 
			The `Listener` class' constructor. Pass in a copy of the `Config` class so
			the `Listener` class can access Quinton's configuration file
		"""

		self.alsaMixer.setvolume(cfg.mic_vol)
		self.recordLen = cfg.ww_detect_time

	# CONTEXT MANAGERS
	#
	# For any context manager, with the form outlined in the contextlib.contextmanager
	# docstring:
	#
	# Everything before the `try` block is prior to context management.
	# Everything in the `try` clause is for variable assignment.
	# Everything in the `finally` clause is for cleanup.

	@staticmethod
	@contextmanager
	def __openstream(paInst: PyAudio, fmt: paInt16, chnls: int, rate: int, sinput: bool, fpb: int) -> Generator[Stream, None, None]:
		""" 
			A context manager to allow the following construct:

				with __openstream(args) as stream:
					... # Do some work
			
			Which will create a new PyAudio stream with `args`.
		"""

		stream = None
		
		try:
			# The object to yield
			stream = paInst.open(
				format=fmt,
				channels=chnls,
				rate=rate,
				input=sinput,
				frames_per_buffer=fpb
			)
			
			yield stream
		finally:
			# Do some cleanup
			stream.stop_stream()
			stream.close()
			
			paInst.terminate()
			
			# Allow time for PyAudio to free the microphone so the SpeechRecognition library
			# can take over
			sleep(1)

	@staticmethod
	@contextmanager
	def __openwf(filepath: str, mode: str) -> Generator[wave.Wave_write, None, None]:
		""" 
			A context manager to allow the following construct:

				with __openwf(args) as stream:
					... # Do some work
			
			Which will open a new wave.Wave_write file with `args`.
		"""

		wf = None

		try:
			wf = wave.open(filepath, mode)
			yield wf
		finally:
			wf.close()

	def liveListen(self) -> Path:
		""" 
			Records `self.recordLen` (default: 2) seconds of live audio to be tested. Returns the path to which the 
			audio was saved.
		"""

		# The audio will be saved in `../data/tmp`, because the output is temporary, 
		# and will be changing constantly.
		SAVE_PATH = Path(f"../data/tmp/llout.wav")

		# Some data needed for recording the audio
		CHUNK = 1024
		FORMAT = paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = self.recordLen
		OUTPUT = SAVE_PATH

		pa = PyAudio()

		with self.__openstream(pa, FORMAT, CHANNELS, RATE, True, CHUNK) as stream:
			print("Recording...")

			frames = list()

			for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.read(CHUNK)
				frames.append(data)

			stream.stop_stream()
			stream.close()
			
			pa.terminate()

			print("Done!")

		with self.__openwf(str(OUTPUT), "wb") as wf:
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(pa.get_sample_size(FORMAT))
			wf.setframerate(RATE)
			wf.writeframes(b"".join(frames))
		
		del pa

		return OUTPUT

	@staticmethod
	def __getRMS(*, file: Path) -> float:
		""" 
			Get the Root-Mean-Square (RMS) value of the recorded audio using the SoX
			command line tool. 
		"""
		
		SOXOUT_PATH = Path("../data/tmp/soxout.txt")

		# Run SoX on the recorded audio file, and save output to `../data/tmp`
		subprocess.call([f"sox {str(file)} -n stat 2> {str(SOXOUT_PATH)}"], shell=True)

		# Manipulate the output to pull only the RMS value. Use the following command:
		# `sed -n '9p' ../data/tmp/soxout.txt | cut -d ':' -f2 | tr -d " \t"`
		rms = float(subprocess.check_output(f"sed -n '9p' {SOXOUT_PATH} | cut -d ':' -f2 | tr -d \" \t\"", shell=True).decode("utf-8"))

		return rms

	def calcIntensity(self, *, audioPath: Path) -> (int, bool):
		"""
			Calculates an audio file's intensity in decibels from its RMS value and
			determines if the decibel level is within the range for normal speech.
		"""
		# Get the RMS value of the audio
		rms = self.__getRMS(file=audioPath)
		
		# Calculate the intensity in decibels from the RMS value
		I_dB = self.__I_dB(rms)

		# The decibel intensity for speaking is usually between 50 and 70 dB. Check to see if the audio
		# intensity is withing those bounds. Intensity levels close to the min and max range values (within +- 2)
		# will be accepted as speech.
		MIN_TSHLD = 50
		MAX_TSHLD = 70

		LEEWAY = 2

		dbrange = range(MIN_TSHLD, MAX_TSHLD)

		inRange: bool

		# If the decibel value is not in the range of intensity of speech, check to see if it is within
		# the +- 2 leeway for decibel values.
		if not I_dB in dbrange:
			if (math.isclose(I_dB, MIN_TSHLD, rel_tol=LEEWAY)) or (math.isclose(I_dB, MAX_TSHLD, rel_tol=LEEWAY)):
				# Round the decibel value to the tens place. 
				# Rounding results:
				# 48 & 49 -> `MIN_TSHLD` (50)
				# 71 & 72 -> `MAX_TSHLD` (70)
				#
				# Using -1 as the `ndigits` argument achieves the result of rounding the the tens place. In Python's
				# rounding function, 0 is the tenths place, 1 doesn't change the number, and -1 is the ones place, so if 
				# a number `n` has a number `x` in the ones place and `x >= 5`, `n` is rounded to the tens place.
				I_dB = int(round(I_db, ndigits=-1))
				inRange = True
			else:
				inRange = False
		else:
			inRange = True

		return (I_dB, inRange)

	@staticmethod
	def __I_dB(p: float, p_0=__PRESSURE_TSHLD) -> float:
		"""
			Formula to use the RMS value to covert to decibels. The original formula is ` I_dB = 20 * log( p/p_0 )`,
			where `p` is the RMS value, `p_0` is the minimum pressure threshold, and `I_dB` is the answer - intensity in
			decibels.
		"""
		try:
			return round((20 * (math.log10((p / p_0)))))
		except ValueError:
			# In case of a strange occurrence (such as a log of 0), return 0.0.
			# This would most likely happen in the case of a muted microphone.
			return 0.0
