#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX"
    sudo apt-get install -y liblo
    echo "END LINUX"
  ;;
  osx)
    echo "START OSX"
    brew install python
    brew link --overwrite python
    brew install liblo
    echo "END OSX"
  ;;
esac

sudo pip install Cython
sudo pip install pyliblo
sudo pip install pyinstaller
sudo pip install -r 3rdparty/pydular/requirements.txt
