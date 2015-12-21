# lekture
lekture is an osc sequencer

this is a work in progress… don't expect a working version in the following weeks ;-)

Development is done under python 2.7.

##Install
You need to install PyQt5, PyOSC and PyBonjour module. The simplest way to install PyQt5 is with using brew.

###Install Brew (OSX)

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

###Install Dependancies

    brew install python
    brew install PyQt5 --with-python --without-python3
    pip install PyOSC

##Build Application

    pip install pyinstaller
    pyinstaller --windowed --icon=icon/lekture.icns lekture.py

##Licence
GPL Licence

##Credits
Produced and Developped by Pixel Stereo
* *icon by WOLF LΔMBERT*

