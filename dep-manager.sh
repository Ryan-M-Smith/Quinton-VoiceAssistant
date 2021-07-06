#!/bin/bash
#!/bin/sh
#!/bin/dash
#!/usr/bin/fish
#!/bin/zsh
#
# FILENAME: dep-install.sh
# DESCRIPTION: Install non-Python dependencies for various Linux distributions.
#
# Supported package managers:
# APT (`apt-get)
# YUM (`yum`)
# DNF (`dnf`)
# Pacman (`pacman`)
# Homebrew (`brew`)
#

# Install dependencies
dep_install () {
	if [ -f /usr/bin/apt-get ]; then # apt-get
		xargs sudo apt-get install --assume-yes < pkglists/pkglist-apt-brew.txt
	elif [ -f /usr/bin/yum ]; then # YUM
		xargs sudo yum install --assumeyes < pkglists/pkglist-yum-dnf.txt
	elif [ -f /usr/bin/dnf ]; then # DNF
		xargs sudo dnf install --assumeyes < pkglists/pkglist-yum-dnf.txt
	elif [ -f /usr/bin/pacman ]; then # Pacman
		xargs sudo pacman -S --needed --noconfirm < pkglists/pkglist-pacman.txt
	elif [[ $(/usr/local/ | grep -c brew) > 0 || \
			$(/opt/homebrew/ | grep -c brew) > 0 || \
			$(/usr/bin/ | grep -c brew) > 0 ]]		# Homebrew
	then
		xargs brew install < pkglists/pkglist-apt-brew.txt
	fi
}

# Uninstall dependencies
dep_uninstall () {
	if [ -f /usr/bin/apt-get ]; then # apt-get
		xargs sudo apt-get remove --assume-yes < pkglists/pkglist-apt-brew.txt
	elif [ -f /usr/bin/yum ]; then # YUM
		xargs sudo yum uninstall --assumeyes < pkglists/pkglist-yum-dnf.txt
	elif [ -f /usr/bin/dnf ]; then # DNF
		xargs sudo dnf uninstall --assumeyes < pkglists/pkglist-yum-dnf.txt
	elif [ -f /usr/bin/pacman ]; then # Pacman
		xargs sudo pacman -S --needed --noconfirm < pkglists/pkglist-pacman.txt
	elif [[ $(/usr/local/ | grep -c brew) > 0 || \
			$(/opt/homebrew/ | grep -c brew) > 0 || \
			$(/usr/bin/ | grep -c brew) > 0 ]]		# Homebrew
	then
		xargs brew uninstall < pkglists/pkglist-apt-brew.txt
	fi
}

# Run everything
if [[ $1 == "install" ]]; then
	dep_install
elif [[ $1 == "uninstall" ]]; then
	dep_uninstall
fi

exit 0
