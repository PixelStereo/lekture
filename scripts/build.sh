#!/bin/sh

pip install -r ../3rdparty/pydular/requirements.txt
pyinstaller --onefile --paths ../3rdparty/pydular/ --windowed --icon=icon/lekture.icns -n Lekture_$1 main.py