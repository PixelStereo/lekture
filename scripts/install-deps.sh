#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX"
    sudo apt-get install ruby
    yes '' | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"
    sudo apt-get install -y build-essential
    export PATH="$HOME/.linuxbrew/bin:$PATH"
    export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
    export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
    which python
    echo "END LINUX"
   ;;
  osx)
    echo "START OSX"
    which python
    echo "END OSX"
  ;;
esac
brew install python
brew install PyQt5 --with-python --without-python3
sudo pip install --pre pyOSC
sudo pip install pjlink
sudo pip install pyinstaller
echo "install-deps END"