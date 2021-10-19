#! /usr/bin/env python3,
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, QSignalMapper, Slot
from PySide6.QtWidgets import QLabel, QLineEdit, QSpinBox, QComboBox, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QListWidget, QAbstractItemView, QPushButton, QGridLayout, QCheckBox

from pylekture import project
#from pylekture.constants import protocols


class EventTable(QTableWidget):
    """
    Table to display Event or Scenario
    """
    def __init__(self):
        super(EventTable, self).__init__()
        self.signalMapper = QSignalMapper(self)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropOverwriteMode(False)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.last_drop_row = None
        self.ttype = None

    @property
    def ttype(self):
        """
        type scenario or events
        """
        return self._ttype
    @ttype.setter
    def ttype(self, ttype):
        print("HERE-IS-HTE-DEBIUG", ttype)
        if isinstance == 'scenario' or isinstance == 'events':
            self._ttype = ttype
            return True

    # Override this method to get the correct row index for insertion
    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        return True

    def dropEvent(self, event):
        # The QTableWidget from which selected rows will be moved
        sender = event.source()
        print("new drag from", sender, "to", self)

        # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
        super(EventTable, self).dropEvent(event)
        # Now we know where to insert selected row(s)
        dropRow = self.last_drop_row
        print("new line in", dropRow)

        selectedRows = sender.getselectedRowsFast()

        # Allocate space for transfer
        for _ in selectedRows:
            self.insertRow(dropRow)

        # if sender == receiver (self), after creating new empty rows selected rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        for i, srow in enumerate(selectedRows):
            for j in range(self.columnCount()):
                item = sender.item(srow, j)
                if item:
                    source = QTableWidgetItem(item)
                    self.setItem(dropRow + i, j, source)

        # delete selected rows
        for srow in reversed(selectedRows):
            sender.removeRow(srow)
        event.accept()


    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows


def create_panels(self):
    # Create Project Attributes layout
    self.project_group = createProjectAttrGroupBox(self)
    # Create Scenario List layout
    ScenarioListGroupBox = createScenarioListGroupBox(self)
    # Create Scenario Attributes layout
    self.scenario_events_group = create_scenario_events_group(self)
    # Create Events Bin
    self.events_list_group = create_events_list_group(self)
    # Create Outputs layout
    # revamp
    #outputs_group = createOuputAttrGroupBox(self)
    #self.outputs_group = outputs_group
    #outputs_group.setVisible(False)
    #self.protocol_display()

    # Create the main layout
    mainLayout = QGridLayout()
    # Integrate the layout previously created
    self.project_group.setMaximumHeight(80)
    mainLayout.addWidget(self.project_group, 0, 0, 1, 1)
    mainLayout.addWidget(ScenarioListGroupBox, 1, 0, 1, 1)
    mainLayout.addWidget(self.events_list_group, 0, 1, 3, 1)
    mainLayout.addWidget(self.scenario_events_group, 2, 0, 1, 1)
    # revamp
    #mainLayout.addWidget(outputs_group, 2, 0, 1, 1)

    # Integrate main layout to the main window
    self.setLayout(mainLayout)
    #self.setMaximumWidth(1222)

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
    project_layout.addWidget(project_path, 0, 0, 1, 3)
    project_layout.addWidget(project_play, 1, 0, 1, 1)
    project_layout.addWidget(project_autoplay, 1, 2, 1, 1)
    project_layout.addWidget(project_loop, 1, 3, 1, 1)
    #project_layout.addStretch(1)
    project_Groupbox.setLayout(project_layout)
    return project_Groupbox

def createScenarioListGroupBox(self):
    ScenarioListGroupBox = QGroupBox("Scenario List")
    self.scenario_list = EventTable()
    self.scenario_list.ttype = "scenario"
    self.scenario_list.signalMapper.mappedObject.connect(self.output_changed)
    self.scenario_list.setSelectionMode(QAbstractItemView.SingleSelection)
    header_list = ['name', 'wait','duration','post_wait', 'loop', 'output']
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
    ScenarioListGroupBox.setLayout(scenarios)
    #ScenarioListGroupBox.setMaximumWidth(576)
    return ScenarioListGroupBox


def create_scenario_events_group(self):
    scenario_events_group = QGroupBox("Selected Scenario")
    # Assign an output to the seleted scenario
    self.scenario_output_label = QLabel('output')
    # Display the selected output
    self.scenario_output_text = QLabel('')
    # Description of the seleted scenario
    self.scenario_description_label = QLabel('description')
    self.scenario_description = QLineEdit()
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
    self.event_del = QPushButton('remove')
    self.event_del.setMaximumWidth(100)
    self.event_del.setDisabled(True)

    self.scenario_description.textEdited.connect(self.scenario_description_changed)
    self.scenario_content.itemChanged.connect(self.scenario_content_changed)
    self.event_play.released.connect(self.event_play_func)
    self.event_del.released.connect(self.event_delete)
    self.scenario_content.itemSelectionChanged.connect(self.eventSelectionChanged)

    layout = QGridLayout()
    layout.addWidget(self.scenario_description_label, 0, 0)
    layout.addWidget(self.scenario_description, 0, 1, 1, 9)
    layout.addWidget(self.scenario_output_label, 1 , 0)
    layout.addWidget(self.scenario_output_text, 1, 1)
    layout.addWidget(self.event_play, 2, 0)
    layout.addWidget(self.event_del, 2, 1)
    layout.addWidget(self.scenario_content_label,3 ,0 )
    layout.addWidget(self.scenario_content, 4, 0, 9, 9)
    scenario_events_group.setLayout(layout)
    return scenario_events_group

def createOuputAttrGroupBox(self):
    # revamp
    #outputs_group = QGroupBox("Outputs")
    # creare a menu to chosse which protocol to display
    self.protocol = QComboBox()
    # revamp
    #for protocol in protocols:
    #    self.protocol.addItem(protocol)
    self.protocol.addItem('OSC')
    # create a button for creating a new output
    self.output_new = QPushButton('New')
    self.output_del = QPushButton('Delete')
    self.output_del.setDisabled(True)
    output_list_header = ['name', 'description', 'service', 'port']
    self.output_list_header = output_list_header
    # create the table to display outputs for each protocols
    protocol_table = QTableWidget(len(self.project.outputs),len(output_list_header))
    protocol_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    for i in range(len(output_list_header)):
        if output_list_header[i] == 'name' or output_list_header[i] == 'description' or output_list_header[i] == 'output' or output_list_header[i] == 'command':
            protocol_table.setColumnWidth(i,140)
        else:
            protocol_table.setColumnWidth(i,55)
    for header in output_list_header:
        head = QTableWidgetItem(header)
        protocol_table.setHorizontalHeaderItem(output_list_header.index(header),head)
    self.protocol_table = protocol_table
    # to get current and previous
    protocol_table.currentItemChanged.connect(self.output_selection_changed)
    # connect any edition in the view to the model update
    self.protocol_table.cellChanged.connect(self.output_table_changed)
    # create a new output
    self.output_new.released.connect(self.new_output_func)
    # delete an output
    self.output_del.released.connect(self.del_output_func)
    # display protocol
    self.protocol.currentIndexChanged.connect(self.protocol_display)

    output_layout = QGridLayout()
    output_layout.addWidget(self.output_new, 0, 0, 1, 1)
    output_layout.addWidget(self.output_del, 0, 1, 1, 1)
    output_layout.addWidget(self.protocol, 0, 2, 1, 1)
    output_layout.addWidget(self.protocol_table, 1, 0, 5, 5)
    outputs_group.setLayout(output_layout)
    return outputs_group

def create_events_list_group(self):
    EventsBinGroupBox = QGroupBox("Events Bin")
    self.events_list_table = EventTable()
    self.events_list_table.ttype = "events"
    self.events_list_table.setSelectionMode(QAbstractItemView.SingleSelection)
    #self.events_list_table.setSortingEnabled(True)
    header_list = ['type', 'name', 'command', 'wait','duration','post_wait', 'loop', 'output']
    self.events_list_header = header_list
    self.events_list_table.setColumnCount(len(header_list))
    for i in range(len(header_list)):
        if header_list[i] == 'name' or header_list[i] == 'description' or header_list[i] == 'output' or header_list[i] == 'command':
            self.events_list_table.setColumnWidth(i,140)
        else:
            self.events_list_table.setColumnWidth(i,55)
    for header in header_list:
        head = QTableWidgetItem(header)
        self.events_list_table.setHorizontalHeaderItem(header_list.index(header), head)
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
    self.event_list_service = QComboBox()
    for service in ['Osc', 'ScenarioPlay', 'Wait', 'MidiNote' ]:
        self.event_list_service.addItem(service)

    events = QGridLayout()
    events.addWidget(self.event_list_new,0,0)
    events.addWidget(self.event_list_play,0,1)
    events.addWidget(self.event_list_del,0,2)
    events.addWidget(self.event_list_service,0,3)
    events.addWidget(self.events_list_table,1,0,5,5)
    EventsBinGroupBox.setLayout(events)
    #EventsBinGroupBox.setMaximumWidth(690)
    return EventsBinGroupBox

