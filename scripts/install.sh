#!/bin/sh

set -v

brew install PyQt5 --with-python --with-python3
sudo pip install Cython
sudo pip3 install Cython
sudo pip install pyliblo
sudo pip3 install pyliblo
sudo pip install pyinstaller
sudo pip3 install pyinstaller
sudo pip install -r 3rdparty/pydular/requirements.txt
sudo pip3 install -r 3rdparty/pydular/requirements.txt

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
