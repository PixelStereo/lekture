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

# install pylekture dependancies
sudo pip3 install -r ../3rdparty/pylekture/requirements.txt
sudo pip3 install pyinstaller

# build the binary
pyinstaller --onefile --paths ../3rdparty/pylekture/ --windowed --icon=icon/icon.icns -n $NAME main.py