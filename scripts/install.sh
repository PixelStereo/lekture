#!/bin/sh

set -v

cd ${HOME}
case "$TRAVIS_OS_NAME" in
  linux)
  echo 'this is linux, so apt-get'
  sudo apt-get -y install python-qt5
  echo "import PyQt5" |python
  
   ;;
  osx)
  echo 'this is osx, so brew'
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install PyQt5
  ;;
esac
cd -

pip install pyproject
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py