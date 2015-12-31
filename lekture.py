#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QDialog,QMenu
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox,QTableWidget

lib_path = os.path.abspath('./lib')
sys.path.append(lib_path)

# import main_window
from main_window import MainWindow

# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../PyProjekt')
sys.path.append(projekt_path)

from pyprojekt import projekt

debug = True
projekt.debug = True
projekt.test = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
