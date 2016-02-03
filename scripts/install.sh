#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    export PATH="$HOME/.linuxbrew/bin:$PATH"
    export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
    export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
    brew install PyQt5 --with-python --without-python3
   ;;
  osx)
    brew install PyQt5 --with-python --without-python3
  ;;
esac

cd src
../scripts/build.sh ${TRAVIS_TAG}
cd dist

case "$TRAVIS_OS_NAME" in
  linux)
    zip Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}
   ;;
  osx)
    zip -r Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}.app
  ;;
esac


cd ../
#python3 main.py
