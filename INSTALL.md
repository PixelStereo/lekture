##Build Statics
http://pyqt.sourceforge.net/Docs/pyqtdeploy/static_builds.html

specifier X.10 à XCODE

    SYSROOT=/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/
    export SYSROOT

    cd qt-everywhere-opensource-src-5.5.1/
    ./configure -prefix $SYSROOT/qt.5.5.1 -static -release -nomake examples
    make -j 8
    make install

    cd ../Python-2.7.11/
    pyqtdeploycli --package python configure
    qmake SYSROOT=$SYSROOT
    make -j 8

    cd ../sip-4.17/
    pyqtdeploycli --package sip configure
    python configure.py --static --sysroot=$SYSROOT --no-tools --use-qmake --configuration=sip-osx.cfg
    /usr/local/Cellar/qt5/5.5.1_2/bin/qmake
    make -j 8
    make install

    cd ../PyQt-gpl-5.5.1/
    pyqtdeploycli --package pyqt5 --target osx-64 configure
    python configure.py --static --sysroot=$SYSROOT --no-tools --no-qsci-api --no-designer-plugin --no-qml-plugin --configuration=pyqt5-osx.cfg 
    make -j 8
    make install
    
    cd ../
    pyqtdeploy Lekture.pdy
