#!/bin/sh

set -e

pyinstaller --windowed --icon=icon/lekture.icns -n 'lecture 0.2' ../lekture.py