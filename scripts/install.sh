#!/bin/sh

set -v

cd src
pyinstaller --windowed --icon=icon/lekture.icns -n Lekture_${TRAVIS_TAG} main.py

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX INSTALL"
      wget http://www.cmake.org/files/v3.2/cmake-3.2.2-Linux-x86_64.tar.gz
      tar -xzf cmake-3.2.2-Linux-x86_64.tar.gz
      mv cmake-3.2.2-Linux-x86_64 cmake
      git clone https://github.com/avilleret/mingw-w64-build ${HOME}/mingw-w64-install
    echo "END LINUX INSTALL"
   ;;
  osx)
    echo "START OSX INSTALL"
    cp functions.py dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp panels.py dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp child.py dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp functions.py dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    wget https://github.com/PixelStereo/PyProjekt/archive/master.zip
    ls
    unzip master.zip
    mv PyProjekt-master/pyprojekt dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cd dist
    zip -r lekture_${TRAVIS_TAG}_OSX.zip lekture_${TRAVIS_TAG}.app
    echo "END OSX INSTALL"
  ;;
esac
cd ../
