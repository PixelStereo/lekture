#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QDialog,QMenu
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox,QTableWidget

# for development of pyprojekt, use git version
import os,sys
lib_path = os.path.abspath('./../PyProjekt')
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
        self.setFixedSize(350,350)
        self.move(pos)
        # create Outputs Interface
        self.createOuputAttrGroupBox()


    def createOuputAttrGroupBox(self):
        self.outputs_GroupBox = QGroupBox("Outputs")
        output_selector_label = QLabel('Output')
        output_protocol = QComboBox()
        for protocol in projekt.protocol_list:
            output_protocol.addItem(protocol)
        output_selector = QSpinBox()
        output_selector.setMinimumSize(50,20)
        output_ip_label = QLabel('IP address')
        output_ip = QLineEdit()
        output_udp_label = QLabel('UDP port')
        output_udp = QSpinBox()
        output_udp.setRange(0,65536)
        output_name_label = QLabel('name (optional)')
        output_name = QLineEdit()
        output_new = QPushButton('New Output')

        self.output_selector = output_selector
        self.output_udp = output_udp
        self.output_ip = output_ip
        self.output_protocol = output_protocol
        self.output_name = output_name
        self.output_new = output_new

        self.output_selector.valueChanged.connect(self.output_selector_changed)
        output_selector.setValue(1)
        output_selector.setRange(1,len(self.project.outputs()))
        
        self.output_new.released.connect(self.output_new_func)
        self.output_name.textEdited.connect(self.output_name_changed)
        self.output_protocol.currentIndexChanged.connect(self.output_protocol_changed)
        self.output_ip.textEdited.connect(self.output_ip_changed)
        self.output_udp.valueChanged.connect(self.output_udp_changed)

        output_layout = QGridLayout()
        output_layout.addWidget(output_new, 0, 0)
        output_layout.addWidget(output_protocol, 0, 1)
        output_layout.addWidget(output_selector_label)
        output_layout.addWidget(output_selector)
        output_layout.addWidget(output_ip_label)
        output_layout.addWidget(output_ip)
        output_layout.addWidget(output_udp_label)
        output_layout.addWidget(output_udp)
        output_layout.addWidget(output_name_label)
        output_layout.addWidget(output_name)
        #output_layout.addStretch(1)

        self.setLayout(output_layout)
        self.setWindowTitle("Output")
        self.resize(650, 400)
        self.exec_()

    def output_new_func(self):
        # create a new output
        self.project.new_output()
        # refresh display
        self.outputs_refresh()
        # select new output that have been just created
        last = len(self.project.outputs()) + 1
        self.output_selector.setValue(last)

    def outputs_refresh(self):
        self.output_clear()
        self.output_selector.setRange(1,len(self.project.outputs()))
        """todo:: update scenario outputs available / NEXT LINE"""
        #self.scenario_output_index.setRange(1,len(self.project.outputs()))
        self.output_display(self.output_selected)

    def output_selector_changed(self,index):
        self.output_clear()
        if self.project.outputs():
            index = index - 1
            output = self.project.outputs()[index]
            # Important to first set output_selected before output_display
            self.output_selected = output
            self.output_display(output)
        else:
            self.output_selected = None

    def output_display(self,output):
        if output:
            self.output_ip.setText(output.ip)
            self.output_udp.setValue(output.udp)
            self.output_name.setText(output.name)

    def output_clear(self):
        self.output_udp.clear()
        self.output_name.clear()
        self.output_ip.clear()

    def output_name_changed(self):
        if self.output_selected:
            self.output_selected.name = self.output_name.text()

    def output_udp_changed(self):
        if self.output_selected:
            self.output_selected.udp = self.output_udp.value()

    def output_ip_changed(self):
        if self.output_selected:
            self.output_selected.ip = self.output_ip.text()

    def output_protocol_changed(self,index):
        if self.output_selected:
            if index != 0:
                print 'ONLY OSC PROTOCOL IS AVAILABLE FOR NOW'
            #self.output_selected.protocol = self.output_protocol.text()

