#! /usr/bin/env python,
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel,QLineEdit,QSpinBox,QComboBox,QTableWidget,QVBoxLayout
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QListWidget,QAbstractItemView,QPushButton,QGridLayout

import os,sys
# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../../PyProjekt')
sys.path.append(projekt_path)

from pyprojekt import projekt
 
def createProjectAttrGroupBox(self):
    self.project_Groupbox = QGroupBox()
    project_layout = QHBoxLayout()
    project_author_label = QLabel('author')
    project_author_label.setMinimumSize(80,10)
    project_author = QLineEdit(self.project.author)
    project_version_label = QLabel('version')
    project_version = QLineEdit(self.project.version)
    project_path_label = QLabel('path')
    project_path = QLabel(self.project.path)
    project_path.setFixedWidth(400)

    self.project_author = project_author
    self.project_version = project_version
    self.project_path = project_path

    self.project_author.textEdited.connect(self.project_author_changed)
    self.project_version.textEdited.connect(self.project_version_changed)

    project_layout.addWidget(project_author_label)
    project_layout.addWidget(project_author)
    project_layout.addWidget(project_version_label)
    project_layout.addWidget(project_version)
    project_layout.addWidget(project_path_label)
    project_layout.addWidget(project_path)
    project_layout.addStretch(1)
    self.project_Groupbox.setLayout(project_layout)   

def createScenarioListGroupBox(self):
    self.ScenarioListGroupBox = QGroupBox("Scenario List")
    self.scenario_list = QListWidget()
    # to get current and previous
    self.scenario_list.currentItemChanged.connect(self.scenarioSelectionChanged)
    # enable drag and drop for internal move aka ordering
    self.scenario_list.setDragDropMode(QAbstractItemView.InternalMove)
    # détournement de la méthode dropEvent du QListWidget
    self.scenario_list.setDropIndicatorShown(True)
    self.scenario_list.setDefaultDropAction(Qt.MoveAction)
    self.scenario_list.dropEvent = self.scenario_list_orderChanged
    # Function to edit scenario's name when double-clicking on it
    self.scenario_list.itemDoubleClicked.connect(self.scenario_list.editItem)
    # Function to rename a scenario if its name changed
    self.scenario_list.itemChanged.connect(self.scenario_name_changed)
    # Button to create a new scenario
    #self.scenario_list.setMinimumSize(120,290)
    self.scenario_new = QPushButton(('New Scenario'))
    self.scenario_new.released.connect(self.newScenario)
    self.scenario_play = QPushButton(('Play Scenario'))
    self.scenario_play.setDisabled(True)
    self.scenario_play.released.connect(self.playScenario)
    self.scenario_del = QPushButton(('Delete Scenario'))
    self.scenario_del.setDisabled(True)
    self.scenario_del.released.connect(self.delScenario)

    layout = QGridLayout()
    layout.addWidget(self.scenario_new,1,0)
    layout.addWidget(self.scenario_play,2,0)
    layout.addWidget(self.scenario_list,3,0)
    layout.addWidget(self.scenario_del,4,0)
    layout.setRowStretch(4, 1)
    layout.setColumnStretch(0, 1)
    self.ScenarioListGroupBox.setLayout(layout)  

def createScenarioAttrGroupBox(self):
    self.ScenarioAttrGroupBox = QGroupBox("Scenario Content")
    # Assign an output to the seleted scenario
    self.scenario_output_label = QLabel('output')
    self.scenario_output_index = QSpinBox()
    self.scenario_output_index.setMinimumSize(50,20)
    self.scenario_output_index.setDisabled(True)
    self.scenario_output_index.setRange(1,len(self.project.outputs()))
    self.scenario_output_protocol = QComboBox()
    self.scenario_output_protocol.addItem('OSC')
    self.scenario_output_protocol.addItem('PJLINK')
    self.scenario_output_protocol.addItem('MIDI')
    self.scenario_output_protocol.addItem('ARTNET')
    self.scenario_output_protocol.setDisabled(True)
    # Display the selected output
    self.scenario_output_text = QLabel('')
    # Description of the seleted scenario
    self.scenario_description_label = QLabel('description')
    self.scenario_description = QLineEdit()
    self.scenario_description.setMinimumSize(450,20)
    self.scenario_description.setDisabled(True)
    # List of the events of the selected scenario
    self.scenario_content_label = QLabel('Events')
    self.scenario_content = QListWidget()
    self.scenario_content.setContextMenuPolicy(Qt.CustomContextMenu)
    self.scenario_content.customContextMenuRequested.connect(self.event_right_click)
    self.scenario_content.setDisabled(True)
    # Button to play the selected event
    self.event_play = QPushButton('play event')
    self.event_play.setMaximumWidth(100)
    self.event_play.setDisabled(True)
    # Button to delete the selected event
    self.event_del = QPushButton('delete event')
    self.event_del.setMaximumWidth(100)
    self.event_del.setDisabled(True)

    self.scenario_output_index.valueChanged.connect(self.scenario_output_index_changed)
    self.scenario_output_protocol.currentTextChanged.connect(self.scenario_output_protocol_changed)
    self.scenario_description.textEdited.connect(self.scenario_description_changed)
    self.scenario_content.itemChanged.connect(self.scenario_content_changed)
    self.event_play.released.connect(self.event_play_func)
    self.event_del.released.connect(self.event_delete)
    self.scenario_content.itemSelectionChanged.connect(self.eventSelectionChanged)

    layout = QGridLayout()
    layout.addWidget(self.scenario_description_label, 0, 0)
    layout.addWidget(self.scenario_description, 0, 1, 1, 9)
    layout.addWidget(self.scenario_output_label,1 , 0)
    layout.addWidget(self.scenario_output_protocol, 1, 1)
    layout.addWidget(self.scenario_output_index, 1, 2)
    layout.addWidget(self.scenario_output_text,1,3)
    layout.addWidget(self.scenario_content_label,2 ,0 )
    layout.addWidget(self.scenario_content, 2, 1, 9, 9)
    layout.addWidget(self.event_play, 8, 0)
    layout.addWidget(self.event_del, 9, 0)
    layout.setRowStretch(8, 1)
    self.ScenarioAttrGroupBox.setLayout(layout)

def createOuputAttrGroupBox(self):
    self.outputs_group = QGroupBox("Outputs")
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
    self.protocol_table = protocol_table
    self.protocol_table.cellChanged.connect(self.dataChanged)
    # create a new output
    self.output_new.released.connect(self.new_output_func)
    # display protocol
    self.protocol.currentIndexChanged.connect(self.protocol_display)
    output_layout = QVBoxLayout()
    output_layout.addWidget(self.output_new)
    output_layout.addWidget(self.protocol)
    output_layout.addWidget(self.protocol_table )
    self.outputs_group.setLayout(output_layout)

    