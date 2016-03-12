#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX"
    sudo apt-get -y install python3 python3-setuptools libpython3.4-dev 
    sudo easy_install3 pip
    sudo apt-get -y install liblo7
    echo "END LINUX"
  ;;
  osx)
    echo "START OSX"
    brew install python3
    brew link --overwrite python3
    brew install liblo
    echo "END OSX"
  ;;
esac

sudo pip3 install Cython
sudo pip3 install pyliblo
sudo pip3 install pyinstaller
