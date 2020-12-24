# FILENAME: dep-install.sh
# DESCRIPTION: Install non-Python dependencies for various Linux distributions.
#
# This script currently supports `apt-get`, `yum`, `dnf`, and `brew` (Homebrew).
#

# Install dependencies
function dep_install { 
	if [ -f /usr/bin/apt-get ]; then # apt-get
		xargs sudo apt-get install --assume-yes < pkglist-apt-brew.txt
	elif [ -f /usr/bin/yum ]; then # YUM
		xargs sudo yum install --assumeyes < pkglist-yum-dnf.txt
	elif [ -f /usr/bin/dnf ]; then # DNF
		xargs sudo dnf install --assumeyes < pkglist-yum-dnf.txt
	elif [[ $(/usr/local/ | grep -c brew) > 0 || \
			$(/opt/homebrew/ | grep -c brew) > 0 || \
			$(/usr/bin/ | grep -c brew) > 0 ]]		# Homebrew
	then
		xargs brew install < pkglist-apt-brew.txt
	fi
}

# Uninstall dependencies
function dep_uninstall {
	if [ -f /usr/bin/apt-get ]; then # apt-get
		xargs sudo apt-get uninstall --assume-yes < pkglist-apt-brew.txt
	elif [ -f /usr/bin/yum ]; then # YUM
		xargs sudo yum uninstall --assumeyes < pkglist-yum-dnf.txt
	elif [ -f /usr/bin/dnf ]; then # DNF
		xargs sudo dnf uninstall --assumeyes < pkglist-yum-dnf.txt
	elif [[ $(/usr/local/ | grep -c brew) > 0 || \
			$(/opt/homebrew/ | grep -c brew) > 0 || \
			$(/usr/bin/ | grep -c brew) > 0 ]]		# Homebrew
	then
		xargs brew uninstall < pkglist-apt-brew.txt
	fi
}

# Run everything
if [[ $0 == "install" ]]; then
	dep_install
elif [[ $0 == "uninstall" ]]; then
	dep_uninstall
fi

exit 0