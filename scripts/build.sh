#!/bin/bash

set -e

pyinstaller --windowed --icon=../icon/lekture.icns -n 'Lekture_'$1 ../lekture.py