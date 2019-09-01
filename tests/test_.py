#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
# for development of pylekture, use git version
pylekture_path = os.path.abspath('./../3rdparty/pylekture')
sys.path.append(pylekture_path)

# for development of pylekture, use git version
lekture_path = os.path.abspath('./../src')
sys.path.append(lekture_path)

import projekt, window

import sys
import unittest

from PySide2.QtWidgets import QApplication
from PySide2 import Qt
from PySide2.Qt import QTest
app = QApplication(sys.argv)

app = window.MainWindow()
#print app.newFile()
projekt.Projekt()
#print(window.project.version, window.project.author)
#scenar = proj.new_scenario()
#print scenar.output()

#QTest.mouseClick(toto.newAct, Qt.LeftButton)