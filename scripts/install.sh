#!/bin/sh

set -v

cd ${HOME}
case "$TRAVIS_OS_NAME" in
  linux)
  echo 'this is linux, so apt-get'
  apt-get install PyQt5
  
   ;;
  osx)
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  echo 'this is osx, so brew'
  ;;
esac
cd -

brew doctor

brew install PyQt5
pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py