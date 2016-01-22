#! /usr/bin/env python,
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel,QLineEdit,QSpinBox,QComboBox,QTableWidget,QVBoxLayout,QTableWidgetItem
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QListWidget,QAbstractItemView,QPushButton,QGridLayout

import os,sys
# for development of pydular, use git version
pydular_path = os.path.abspath('./../../pydular')
sys.path.append(pydular_path)

from pydular import project
 
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
    project_path.setMinimumWidth(400)

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
    self.scenario_list = QTableWidget()
    self.scenario_list.setSelectionMode(QAbstractItemView.SingleSelection)
    header_list = ['name','wait','duration','post_wait','protocol','output']
    self.scenario_list.setColumnCount(len(header_list))
    for i in range(len(header_list)):
        if i == 0:
            self.scenario_list.setColumnWidth(i,250)
        else:
            self.scenario_list.setColumnWidth(i,80)
    for header in header_list:
        head = QTableWidgetItem(header)
        self.scenario_list.setHorizontalHeaderItem(header_list.index(header),head)
    self.scenario_list.setSelectionBehavior(QAbstractItemView.SelectRows)
    # to get current and previous
    self.scenario_list.currentItemChanged.connect(self.scenarioSelectionChanged)
    # Function to edit scenario's name when double-clicking on it
    self.scenario_list.itemDoubleClicked.connect(self.scenario_list.editItem)
    # Function to rename a scenario if its name changed
    self.scenario_list.cellChanged.connect(self.scenario_data_changed)
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
    layout.addWidget(self.scenario_new,0,0)
    layout.addWidget(self.scenario_play,1,0)
    layout.addWidget(self.scenario_del,2,0)
    layout.setRowStretch(5, 1)
    layout.setColumnStretch(0, 5)
    scenario_commands = QGroupBox("Scenario commands")
    scenario_commands.setLayout(layout)  
    scenario_commands.setMinimumWidth(140)
    scenario_commands.setMinimumHeight(150)
    scenario_commands.setMaximumWidth(140)
    scenario_commands.setMaximumHeight(150)
    scenarios = QGridLayout()
    scenarios.addWidget(scenario_commands,0,0)
    scenarios.addWidget(self.scenario_list,0,1,5,5)
    self.ScenarioListGroupBox.setMinimumHeight(250)
    self.ScenarioListGroupBox.setLayout(scenarios)
    

def createScenarioAttrGroupBox(self):
    self.ScenarioAttrGroupBox = QGroupBox("Scenario Content")
    #self.ScenarioAttrGroupBox.setVisible(False)
    # Assign an output to the seleted scenario
    self.scenario_output_label = QLabel('output')
    self.scenario_output_index = QSpinBox()
    self.scenario_output_index.setMinimumSize(50,20)
    self.scenario_output_index.setDisabled(True)
    self.scenario_output_index.setRange(1,len(self.project.outputs()))
    self.scenario_output_protocol = QComboBox()
    for proto in project.Output.protocols():
        self.scenario_output_protocol.addItem(proto)
    self.scenario_output_protocol.setDisabled(True)
    # Display the selected output
    self.scenario_output_text = QLabel('')
    # Description of the seleted scenario
    self.scenario_description_label = QLabel('description')
    self.scenario_description = QLineEdit()
    self.scenario_description.setMinimumSize(250,20)
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
    self.ScenarioAttrGroupBox.setFixedHeight(250)
    self.ScenarioAttrGroupBox.setLayout(layout)

def createOuputAttrGroupBox(self):
    self.outputs_group = QGroupBox("Outputs")
    # creare a menu to chosse which protocol to display
    self.protocol = QComboBox()
    for protocol in project.Output.protocols():
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

    