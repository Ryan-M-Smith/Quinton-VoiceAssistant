# FILENAME: build.sh
# DESCRIPTION: Build a new release of Quinton-VoiceAssistant

declare name="Quinton-VoiceAssistant"
declare master="Quinton-VoiceAssistant-Master"
declare startpt="/home/pi/Projects"

# Make sure there is a place to store releases
if [[ ! -d releases ]]; then
	mkdir $startpt/$master/releases
fi

declare relpt="$startpt/$master/releases/$name-$(sed -n '1p' version.txt)" # Where the release is stored

cd $startpt

cp -r Quinton-VoiceAssistant-Master Quinton-VoiceAssistant # New release

cd Quinton-VoiceAssistant

python3.8 setup.py sdist bdist_wheel # Build a tarball and wheel (Linux)
python3.8 setup.py sdist --formats=zip # Make a zip archive as well. MacOS can use the tarball, but a zip might be easier

mkdir $relpt # Make a new directory for the release

cp dist/* $relpt

cd .. # Move back into `~/Projects`

sudo rm -r $name # Clean up

exit 0
