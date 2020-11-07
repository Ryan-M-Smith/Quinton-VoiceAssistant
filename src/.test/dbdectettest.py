# FILENAME: dbdetecttest.py
# Use Physics formulas regarding sound to calculate a sound's intensity in decibels
import subprocess, math, sys
from typing import NoReturn

def I_dB(p, p_0) -> float:
	"""
		Formula to use the RMS value to covert to decibels. The original formula is `20 * log( p/p_0 ) = I_dB`,
		where `p` is the RMS value, `p_0` is the minimum pressure threshold, and `I_dB` is the answer - intensity in
		decibels.
	"""
	return round((20 * (math.log10((p / p_0)))))

def main() -> NoReturn:
	# The minimum pressure threshold in Pascals, effectively representing 0 dB. Note that
	# The actual decibel value of this number is somewhere around 4 dB, but it is most
	# commonly used as a reference point of 0 dB because decibels are a relative unit, thus
	# requiring such a point.
	PRESSURE_TSHLD = float(2 * math.pow(10, -5))

	# Start with a pre-recorded audio file. Use SoX to get the audio's Root-mean-square.
	rms = float(subprocess.check_output("sed -n '9p' ~/soxout.txt | cut -d ':' -f2 | tr -d \" \\t\"", shell=True, encoding="utf-8"))
	
	# Plug into the formula and solve
	dB = I_dB(rms, PRESSURE_TSHLD)

	print("Intensity in decibels:", dB)

if __name__ == "__main__":
	sys.exit(main())