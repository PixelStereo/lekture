#!/bin/sh

pyinstaller --onefile --paths ../3rdparty/pydular/ --windowed --icon=icon/lekture.icns -n Lekture_$1 main.py