#! /usr/bin/env python,
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QComboBox, QTableWidget, QVBoxLayout, QTableWidgetItem
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QListWidget, QAbstractItemView, QPushButton, QGridLayout, QCheckBox

from pylekture import project
from pylekture.constants import protocols

def createProjectAttrGroupBox(self):
    self.project_Groupbox = QGroupBox()
    project_layout = QHBoxLayout()
    project_version_label = QLabel('version')
    project_version = QLabel(self.project.version)
    project_path_label = QLabel('path')
    project_path = QLabel(self.project.path)
    project_autoplay_label = QLabel('autoplay')
    project_autoplay = QCheckBox()
    project_loop_label = QLabel('loop')
    project_loop = QCheckBox()
    project_play = QPushButton('Play')
    #project_path.setMinimumWidth(400)

    self.project_version = project_version
    self.project_path = project_path
    self.project_autoplay = project_autoplay
    self.project_loop = project_loop
    self.project_play = project_play

    self.project_autoplay.stateChanged.connect(self.project_autoplay_changed)
    self.project_loop.stateChanged.connect(self.project_loop_changed)
    self.project_play.released.connect(self.project_play_action)

    project_layout.addWidget(project_version_label)
    project_layout.addWidget(project_version)
    project_layout.addWidget(project_path_label)
    project_layout.addWidget(project_path)
    project_layout.addWidget(project_play)
    project_layout.addWidget(project_autoplay_label)
    project_layout.addWidget(project_autoplay)
    project_layout.addWidget(project_loop_label)
    project_layout.addWidget(project_loop)
    #project_layout.addStretch(1)
    self.project_Groupbox.setLayout(project_layout)

def createScenarioListGroupBox(self):
    self.ScenarioListGroupBox = QGroupBox("Scenario List")
    self.scenario_list = QTableWidget()
    self.scenario_list.setSelectionMode(QAbstractItemView.SingleSelection)
    header_list = ['name', 'wait','duration','post_wait','output']
    self.scenario_list_header = header_list
    self.scenario_list.setColumnCount(len(header_list))
    for i in range(len(header_list)):
        if header_list[i] == 'name' or header_list[i] == 'description' or header_list[i] == 'output':
            self.scenario_list.setColumnWidth(i,140)
        else:
            self.scenario_list.setColumnWidth(i,60)
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
    # Function to trigger when output menu is changed
    self.scenario_list.cellChanged.connect(self.scenario_data_changed)
    # Button to create a new scenario
    self.scenario_new = QPushButton(('New Scenario'))
    self.scenario_new.released.connect(self.newScenario)
    self.scenario_play = QPushButton(('Play Scenario'))
    self.scenario_play.setDisabled(True)
    self.scenario_play.released.connect(self.playScenario)
    self.scenario_del = QPushButton(('Delete Scenario'))
    self.scenario_del.setDisabled(True)
    self.scenario_del.released.connect(self.delScenario)

    scenarios = QGridLayout()
    scenarios.addWidget(self.scenario_new, 0, 0)
    scenarios.addWidget(self.scenario_play, 0, 1)
    scenarios.addWidget(self.scenario_del, 0, 2)
    scenarios.addWidget(self.scenario_list, 1, 0, 5, 5)
    self.ScenarioListGroupBox.setLayout(scenarios)


def createScenarioAttrGroupBox(self):
    self.ScenarioAttrGroupBox = QGroupBox("Scenario Content")
    #self.ScenarioAttrGroupBox.setVisible(False)
    # Assign an output to the seleted scenario
    self.scenario_output_label = QLabel('output')
    self.scenario_output = QComboBox()
    self.scenario_output.setMinimumSize(50,20)
    self.scenario_output.setDisabled(True)
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

    self.scenario_output.currentIndexChanged.connect(self.scenario_output_changed)
    self.scenario_description.textEdited.connect(self.scenario_description_changed)
    self.scenario_content.itemChanged.connect(self.scenario_content_changed)
    self.event_play.released.connect(self.event_play_func)
    self.event_del.released.connect(self.event_delete)
    self.scenario_content.itemSelectionChanged.connect(self.eventSelectionChanged)

    layout = QGridLayout()
    layout.addWidget(self.scenario_description_label, 0, 0)
    layout.addWidget(self.scenario_description, 0, 1, 1, 9)
    layout.addWidget(self.scenario_output_label,1 , 0)
    layout.addWidget(self.scenario_output, 1, 1)
    layout.addWidget(self.scenario_output_text,1,2)
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
    for protocol in protocols:
        self.protocol.addItem(protocol)
    # create a button for creating a new output
    self.output_new = QPushButton('New Output')
    # create the table to display outputs for each protocols
    protocol_table = QTableWidget(len(self.project.outputs),3)
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
    output_layout.addWidget(self.protocol_table)
    self.outputs_group.setLayout(output_layout)

def createEventsBinGroupBox(self):
    self.EventsBinGroupBox = QGroupBox("Events Bin")
    self.events_bin = QTableWidget()
    self.events_bin.setSelectionMode(QAbstractItemView.SingleSelection)
    header_list = ['name','wait','duration','post_wait','output']
    self.events_bin.setColumnCount(len(header_list))
    for i in range(len(header_list)):
        if header_list[i] == 'name' or header_list[i] == 'description' or header_list[i] == 'output':
            self.events_bin.setColumnWidth(i,140)
        else:
            self.events_bin.setColumnWidth(i,55)
    for header in header_list:
        head = QTableWidgetItem(header)
        self.events_bin.setHorizontalHeaderItem(header_list.index(header),head)
    self.events_bin.setSelectionBehavior(QAbstractItemView.SelectRows)
    # to get current and previous
    self.events_bin.currentItemChanged.connect(self.eventSelectionChanged)
    # Function to edit scenario's name when double-clicking on it
    self.events_bin.itemDoubleClicked.connect(self.events_bin.editItem)
    # Function to rename a scenario if its name changed
    self.events_bin.cellChanged.connect(self.event_data_changed)
    # Button to create a new scenario
    self.event_new = QPushButton(('New'))
    self.event_new.released.connect(self.new_event)
    self.event_play = QPushButton(('Play'))
    self.event_play.setDisabled(True)
    self.event_play.released.connect(self.play_event)
    self.event_del = QPushButton(('Delete'))
    self.event_del.setDisabled(True)
    self.event_del.released.connect(self.event_delete)

    events = QGridLayout()
    events.addWidget(self.event_new,0,0)
    events.addWidget(self.event_play,0,1)
    events.addWidget(self.event_del,0,2)
    events.addWidget(self.events_bin,1,0,5,5)
    self.EventsBinGroupBox.setLayout(events)

