#!/bin/bash

set -e

pyinstaller --windowed --icon=icon/lekture.icns -n 'Lekture '$1 ../lekture.py