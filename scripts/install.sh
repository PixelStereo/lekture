#!/bin/sh

set -v

cd ${HOME}
case "$TRAVIS_OS_NAME" in
  linux)
  echo 'this is linux, so apt-get'
  sudo apt-get install PyQt5
  
   ;;
  osx)
  echo 'this is osx, so brew'
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install PyQt5
  ;;
esac
cd -

pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py