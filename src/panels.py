#! /usr/bin/env python,
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QComboBox, QTableWidget, QVBoxLayout, QTableWidgetItem
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QListWidget, QAbstractItemView, QPushButton, QGridLayout, QCheckBox

from pylekture import project
from pylekture.constants import protocols

def createProjectAttrGroupBox(self):
    project_Groupbox = QGroupBox()
    project_layout = QGridLayout()
    #project_version_label = QLabel('version')
    #project_version = QLabel(self.project.version)
    project_path = QLabel(self.project.path)
    project_autoplay = QPushButton('autoplay')
    project_autoplay.setCheckable(True)
    project_loop = QPushButton('loop')
    project_loop.setCheckable(True)
    project_play = QPushButton('Play')
    #self.project_version = project_version
    self.project_path = project_path
    self.project_autoplay = project_autoplay
    self.project_loop = project_loop
    self.project_play = project_play

    self.project_autoplay.toggled.connect(self.project_autoplay_changed)
    self.project_loop.toggled.connect(self.project_loop_changed)
    self.project_play.released.connect(self.project_play_action)

    #project_layout.addWidget(project_version_label)
    #project_layout.addWidget(project_version)
    project_layout.addWidget(project_path, 0, 0)
    project_layout.addWidget(project_play, 1, 0)
    project_layout.addWidget(project_autoplay, 1, 2)
    project_layout.addWidget(project_loop, 1, 3)
    #project_layout.addStretch(1)
    project_Groupbox.setLayout(project_layout)
    return project_Groupbox

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
    self.scenario_new = QPushButton(('New'))
    self.scenario_new.released.connect(self.new_scenario)
    self.scenario_play = QPushButton(('Play'))
    self.scenario_play.setDisabled(True)
    self.scenario_play.released.connect(self.playScenario)
    self.scenario_del = QPushButton(('Delete'))
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
    self.event_play = QPushButton('play')
    self.event_play.setMaximumWidth(100)
    self.event_play.setDisabled(True)
    # Button to delete the selected event
    self.event_del = QPushButton('delete')
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
    self.ScenarioAttrGroupBox.setLayout(layout)

def createOuputAttrGroupBox(self):
    self.outputs_group = QGroupBox("Outputs")
    # creare a menu to chosse which protocol to display
    self.protocol = QComboBox()
    for protocol in protocols:
        self.protocol.addItem(protocol)
    # create a button for creating a new output
    self.output_new = QPushButton('New')
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
    output_layout = QGridLayout()
    output_layout.addWidget(self.output_new, 0, 0, 1, 1)
    output_layout.addWidget(self.protocol, 0, 1, 1, 4)
    output_layout.addWidget(self.protocol_table, 1, 0, 5, 5)
    self.outputs_group.setLayout(output_layout)

def createEventsBinGroupBox(self):
    EventsBinGroupBox = QGroupBox("Events Bin")
    self.events_list_table = QTableWidget()
    self.events_list_table.setSelectionMode(QAbstractItemView.SingleSelection)
    header_list = ['name','wait','duration','post_wait','output']
    self.events_list_header = header_list
    self.events_list_table.setColumnCount(len(header_list))
    for i in range(len(header_list)):
        if header_list[i] == 'name' or header_list[i] == 'description' or header_list[i] == 'output':
            self.events_list_table.setColumnWidth(i,140)
        else:
            self.events_list_table.setColumnWidth(i,55)
    for header in header_list:
        head = QTableWidgetItem(header)
        self.events_list_table.setHorizontalHeaderItem(header_list.index(header),head)
    self.events_list_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # to get current and previous
    self.events_list_table.currentItemChanged.connect(self.event_list_selection_changed)
    # Function to edit scenario's name when double-clicking on it
    self.events_list_table.itemDoubleClicked.connect(self.events_list_table.editItem)
    # Function to rename a scenario if its name changed
    self.events_list_table.cellChanged.connect(self.event_data_changed)
    # Button to create a new scenario
    self.event_list_new = QPushButton(('New'))
    self.event_list_new.released.connect(self.new_event_list)
    self.event_list_play = QPushButton(('Play'))
    self.event_list_play.setDisabled(True)
    self.event_list_play.released.connect(self.play_event_list)
    self.event_list_del = QPushButton(('Delete'))
    self.event_list_del.setDisabled(True)
    self.event_list_del.released.connect(self.delete_event_list)

    events = QGridLayout()
    events.addWidget(self.event_list_new,0,0)
    events.addWidget(self.event_list_play,0,1)
    events.addWidget(self.event_list_del,0,2)
    events.addWidget(self.events_list_table,1,0,5,5)
    EventsBinGroupBox.setLayout(events)
    return EventsBinGroupBox

