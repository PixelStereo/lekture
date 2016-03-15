#!/bin/sh

# REMEMBER CURRENT DIR
CURRENT="${PWD##*/}"
# GO ONE DIR UP
cd ../
# DEFAULTVALUE FOR THE APP IS THE NAME OF THE REPO
DEFAULTVALUE="${PWD##*/}"
# GO BACK SRC
cd $CURRENT
# COMMAND LINE ARGUMENT OR REPO NAME
NAME=${1:-$DEFAULTVALUE}
echo "app will be build with the name :" $NAME

# linux use pip, and osx use pip3
case "$TRAVIS_OS_NAME" in
  linux)
    sudo pip install -r ../3rdparty/pydular/requirements.txt
  ;;
    osx)
    sudo pip3 install -r ../3rdparty/pydular/requirements.txt
  ;;

esac

pyinstaller --onefile --paths ../3rdparty/pydular/ --windowed --icon=icon/icon.icns -n $NAME main.py