#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    echo "START LINUX"
    sudo apt-get install ruby
    yes '' | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"
    sudo apt-get install -y build-essential
    export PATH="$HOME/.linuxbrew/bin:$PATH"
    export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
    export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
    echo "END LINUX"
   ;;
  osx)
    echo "START OSX"
    echo "END OSX"
  ;;
esac
git submodule init
git submodule update
brew install python
brew install python3
brew install liblo
echo "install-deps END"