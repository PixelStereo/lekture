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
    echo "END LINUX"
   ;;
  osx)
    echo "START OSX"
    echo "nothing to do… brew is already installed on osx"
    echo "END OSX"
  ;;
esac
echo "START install-deps"
brew install python
brew link --overwrite python
brew install python3
brew install liblo
sudo pip install Cython
sudo pip3 install Cython
sudo pip install pyliblo
sudo pip3 install pyliblo
sudo pip install pyinstaller
sudo pip3 install pyinstaller
sudo pip install -r 3rdparty/pydular/requirements.txt
sudo pip3 install -r 3rdparty/pydular/requirements.txt
echo "END install-deps"
