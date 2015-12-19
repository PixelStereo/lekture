#!/bin/sh


if [ "x$TRAVIS_OS_NAME" = "xosx" ]; then
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
  yes '' | ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
fi
brew install PyQt5
pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py