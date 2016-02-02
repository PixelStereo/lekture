#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
# for development of pydular, use git version
pydular_path = os.path.abspath('./../3rdparty/pydular')
sys.path.append(pydular_path)
# for development of pydular, use git version
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