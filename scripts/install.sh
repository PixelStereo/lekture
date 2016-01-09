#!/bin/sh

set -v

cd src
pyinstaller --windowed --icon=icon/lekture.icns -n Lekture_${TRAVIS_TAG} main.py


case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX INSTALL"
    echo "list APP -1"
    ls dist
    echo "list APP 0"
    ls dist/Lekture_${TRAVIS_TAG}/
    cp functions.py dist/Lekture_${TRAVIS_TAG}/
    cp panels.py dist/Lekture_${TRAVIS_TAG}/
    cp child.py dist/Lekture_${TRAVIS_TAG}/
    cp functions.py dist/Lekture_${TRAVIS_TAG}/
    echo "list APP 1"
    ls dist/Lekture_${TRAVIS_TAG}/
    wget https://github.com/PixelStereo/PyProjekt/archive/master.zip
    unzip master.zip
    mkdir dist/Lekture_${TRAVIS_TAG}/pyprojekt
    echo "list APP 2"
    ls dist/Lekture_${TRAVIS_TAG}/
    mv PyProjekt-master/pyprojekt/* dist/Lekture_${TRAVIS_TAG}/pyprojekt/
    cd dist
    zip -r Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}
    sudo rm /home/travis/build.sh
    sudo echo "#!/bin/sh">/home/travis/build.sh
    echo "END LINUX INSTALL"
   ;;
  osx)
    echo "START OSX INSTALL"
    cp functions.py dist/Lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp panels.py dist/Lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp child.py dist/Lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cp functions.py dist/Lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    wget https://github.com/PixelStereo/PyProjekt/archive/master.zip
    ls
    unzip master.zip
    mv PyProjekt-master/pyprojekt dist/lekture_${TRAVIS_TAG}.app/Contents/MacOS/
    cd dist
    zip -r Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}.app
    sudo rm /Users/travis/build.sh
    sudo echo "#!/bin/sh">/Users/travis/build.sh
    echo "END OSX INSTALL"
  ;;
esac

