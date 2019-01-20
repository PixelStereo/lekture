#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main script
"""

import sys
from window import MainWindow
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))


if __name__ == "__main__":
    try:
        #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        pass
    except Exception as error:
        print('failed ' + str(error))
    root = QFileInfo(__file__).absolutePath()
    path = root+'/icon/icon.png'
    app.setWindowIcon(QIcon(path))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
