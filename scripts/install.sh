#!/bin/sh

set -v

cd src
../scripts/build.sh ${TRAVIS_TAG}
cd dist

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX INSTALL"
    ls -lisah
    zip Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}
    sudo rm /home/travis/build.sh
    sudo echo "#!/bin/sh">/home/travis/build.sh
    echo "END LINUX INSTALL"
   ;;
  osx)
    echo "START OSX INSTALL"
    zip -r Lekture_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip Lekture_${TRAVIS_TAG}.app
    sudo rm /Users/travis/build.sh
    sudo echo "#!/bin/sh">/Users/travis/build.sh
    echo "END OSX INSTALL"
  ;;
esac
ls -lisah
