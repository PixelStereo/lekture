#!/bin/sh

set -v

cd src
pyinstaller --windowed --icon=icon/lekture.icns -n Lekture_${TRAVIS_TAG} main.py


case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX INSTALL"
    echo ''
    echo ''
    echo ''
    echo ''
    echo ''
    echo ''
    ls -lisah dist/Lekture_${TRAVIS_TAG}
    echo ''
    echo ''
    echo ''
    sudo rm /home/travis/build.sh
    ls /home/travis
    sudo echo "#!/bin/sh">/home/travis/build.sh
    cat /home/travis/build.sh
    echo ''
    echo ''
    echo ''
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
    sudo rm /Users/travis/build.sh
    ls /Users/travis
    sudo echo "#!/bin/sh">/Users/travis/build.sh
    cat /Users/travis/build.sh
  ;;
esac
cd ../
