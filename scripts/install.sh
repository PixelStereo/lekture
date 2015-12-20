#!/bin/sh

set -v

cd ${HOME}
case "$TRAVIS_OS_NAME" in
  linux)
  yes '' | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"
  echo 'THIS IS A LINUX, so Install dependancies'
  sudo apt-get install build-essential
   ;;
  osx)
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  echo 'THIS IS A MAC'
  ;;
esac
cd -

brew doctor

brew install PyQt5
pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py