#!/bin/sh

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install PyQt5
pip install PyOSC
pip install pyinstaller
pyinstaller --windowed --icon=icon/lekture.icns lekture.py