#!/bin/bash

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    sudo apt-get update
    sudo apt-get -y install python3-pyqt5
  ;;
    osx)
    brew install PyQt5 --without-python --with-python3
  ;;

esac
cd src

source ../scripts/split_repo_slug.sh

../scripts/build.sh ${REPO}_${TRAVIS_TAG}
cd dist 

case "$TRAVIS_OS_NAME" in
  linux)
    zip ${REPO}_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip ${REPO}_${TRAVIS_TAG}
   ;;
  osx)
    zip -r ${REPO}_${TRAVIS_TAG}_$TRAVIS_OS_NAME.zip ${REPO}_${TRAVIS_TAG}.app
  ;;
esac

cd ../
