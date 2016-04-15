#!/bin/sh

# REMEMBER CURRENT DIR
CURRENT="${PWD##*/}"
# GO ONE DIR UP
cd ../
TAG=$(git describe --tags --dirty --long)
# DEFAULTVALUE FOR THE APP IS THE NAME OF THE REPO
DEFAULTVALUE="${PWD##*/}"_$TAG
# GO BACK SRC
cd $CURRENT
# use argument if present (build with travis on tag), or use git sha if no arg provided (local)
NAME=${1:-$DEFAULTVALUE}
echo "app will be build with the name :" $NAME

# install pylekture dependancies
sudo pip3 install -r ../3rdparty/pylekture/requirements.txt
sudo pip3 install pyinstaller

# build the binary
pyinstaller --onefile --paths ../3rdparty/pylekture/ --osx-bundle-identifier org.pixel-stereo.lekture --windowed --icon=icon/icon.icns -n $NAME main.py