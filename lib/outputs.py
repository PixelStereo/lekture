#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QDialog,QMenu,QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox,QTableWidget

# for development of pyprojekt, use git version
import os,sys
lib_path = os.path.abspath('./../../PyProjekt')
sys.path.append(lib_path)

from pyprojekt import projekt

debug = True
projekt.debug = True
projekt.test = False

class OutputsPanel(QDialog):
    """docstring for OutputsPanel"""
    def __init__(self, project,pos):
        super(OutputsPanel, self).__init__()
        self.project = project
        self.setFixedSize(600,350)
        self.move(pos)
        # create Outputs Interface
        self.createOuputAttrGroupBox()
        self.protocol.setCurrentText('OSC')
        self.protocol_display()
        self.setWindowTitle("Outputs")
        self.exec_()

    def createOuputAttrGroupBox(self):
        self.outs_GroupBox = QGroupBox("Outputs")
        # creare a menu to chosse which protocol to display
        self.protocol = QComboBox()
        for protocol in projekt.Output.protocols():
            self.protocol.addItem(protocol)
        # create a button for creating a new output
        self.output_new = QPushButton('New Output')
        # create the table to display outputs for each protocols
        protocol_table = QTableWidget(len(self.project.outputs(protocol='OSC')),3)
        protocol_table.setColumnWidth(0,130)
        protocol_table.setColumnWidth(1,130)
        protocol_table.setColumnWidth(2,130)
        protocol_table.setColumnWidth(3,130)
        protocol_table.setFixedWidth(550)
        self.protocol_table = protocol_table
        self.protocol_table.cellChanged.connect(self.dataChanged)
        # create a new output
        self.output_new.released.connect(self.new_output_func)
        # display protocol
        self.protocol.currentIndexChanged.connect(self.protocol_display)
        output_layout = QGridLayout()
        output_layout.addWidget(self.output_new, 0, 0)
        output_layout.addWidget(self.protocol, 0, 1)
        output_layout.addWidget(self.protocol_table )
        self.setLayout(output_layout)

    def new_output_func(self):
        protocol = self.protocol.currentText()
        self.project.new_output(protocol)
        self.protocol_display()

    def protocol_display(self):
        self.protocol_table.clear()
        protocol = self.protocol.currentText()
        self.protocol_table.setRowCount(len(self.project.outputs(protocol)))
        if protocol:
            row = 0
            for out in self.project.outputs(protocol):
                col = 0
                attrs = out.vars_()
                for attr in attrs:
                    if attr.startswith('_'):
                        attrs.remove(attr)
                attrs.sort()
                if attrs:
                    self.protocol_table.setColumnCount(len(attrs))
                    for attr in attrs:
                        header = QTableWidgetItem(attr)
                        self.protocol_table.setHorizontalHeaderItem(col,header)
                        item = QTableWidgetItem(str(getattr(out,attr)))
                        self.protocol_table.setItem(row,col,item)
                        col = col + 1
                    row = row + 1

    def dataChanged(self,row,col):
        if self.protocol_table.currentItem():
            protocol = self.protocol.currentText()
            outs = self.project.outputs(protocol)
            out = outs[row]
            attr = self.protocol_table.horizontalHeaderItem(col).text()
            value = self.protocol_table.currentItem().text()
            setattr(out,attr,value)

