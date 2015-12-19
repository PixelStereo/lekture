#!/bin/sh


if [ "x$TRAVIS_OS_NAME" = "xosx" ]; then
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  echo 'THIS IS A MAC'
else
  yes '' | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"
  echo 'THIS IS A LINUX'
fi

brew install PyQt5
pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py