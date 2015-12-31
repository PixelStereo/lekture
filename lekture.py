#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath
from sys import path,argv,exit

from PyQt5.QtWidgets import QApplication

# add lib path to python path
lib_path = abspath('./lib')
path.append(lib_path)

# import main_window
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(argv)
    mainWin = MainWindow()
    mainWin.show()
    exit(app.exec_())