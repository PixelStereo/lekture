#!/bin/sh

set -v

cd src
pyinstaller --onefile --paths ../3rdparty/PyProjekt/ --windowed --icon=icon/lekture.icns -n Lekture_${TRAVIS_TAG} main.py
cd dist
zip -r Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}.app

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX INSTALL"
    sudo rm /home/travis/build.sh
    sudo echo "#!/bin/sh">/home/travis/build.sh
    echo "END LINUX INSTALL"
   ;;
  osx)
    echo "START OSX INSTALL"
    sudo rm /Users/travis/build.sh
    sudo echo "#!/bin/sh">/Users/travis/build.sh
    echo "END OSX INSTALL"
  ;;
esac

