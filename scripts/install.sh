#!/bin/sh

set -v

cd ${HOME}
case "$TRAVIS_OS_NAME" in
  linux)
  sudo apt-get -y install pyqt5
  
   ;;
  osx)
  echo 'this is osx, so brew'
  which python
  brew install python
  travis_wait brew install PyQt5 --with-python --without-python3
  sudo pip install --pre pyOSC
  sudo pip install pyprojekt
  sudo pip install pyinstaller
  ;;
esac
cd -

pip install pyproject
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py