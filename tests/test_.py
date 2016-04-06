#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
# for development of pybush, use git version
pybush_path = os.path.abspath('./../3rdparty/pybush')
sys.path.append(pybush_path)

# for development of pybush, use git version
lekture_path = os.path.abspath('./../src')
sys.path.append(lekture_path)

import main

import sys
import unittest

from PyQt5.QtWidgets import QApplication
from PyQt5 import Qt
from PyQt5.Qt import QTest
app = QApplication(sys.argv)

app = main.MainWindow()
#print app.newFile()
main.Projekt()
#print(window.project.version, window.project.author)
#scenar = proj.new_scenario()
#print scenar.output()

#QTest.mouseClick(toto.newAct, Qt.LeftButton)