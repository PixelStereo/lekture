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
        self.setFixedSize(500,350)
        self.move(pos)
        # create Outputs Interface
        self.createOuputAttrGroupBox()


    def createOuputAttrGroupBox(self):
        self.outputs_GroupBox = QGroupBox("Outputs")
        #output_selector_label = QLabel('Output')
        output_protocol = QComboBox()
        for protocol in projekt.protocol_list:
            output_protocol.addItem(protocol)
        output_new = QPushButton('New Output')
        osc_table = QTableWidget(len(self.project.outputs('OSC')),4)
        osc_table.setColumnWidth(0,40)
        osc_table.setColumnWidth(1,120)
        osc_table.setColumnWidth(2,65)
        osc_table.setColumnWidth(3,140)
        osc_table.setFixedWidth(390)

        self.output_protocol = output_protocol
        self.output_new = output_new
        self.osc_table = osc_table
        
        self.output_new.released.connect(self.output_new_func)
        self.output_protocol.currentIndexChanged.connect(self.output_protocol_changed)

        output_layout = QGridLayout()
        output_layout.addWidget(output_new, 0, 0)
        output_layout.addWidget(output_protocol, 0, 1)
        output_layout.addWidget(osc_table )

        self.setLayout(output_layout)
        self.setWindowTitle("Outputs")
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
        self.osc_table.clear()

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

