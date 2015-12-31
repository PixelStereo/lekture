#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QLabel,QLineEdit,QListWidget,QAbstractItemView,QPushButton,QGridLayout,QSpinBox,QComboBox,QFileDialog,QListWidgetItem,QApplication,QMessageBox
from PyQt5.QtCore import Qt,QModelIndex,QFileInfo

# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../../PyProjekt')
sys.path.append(projekt_path)

from pyprojekt import projekt

class Document(object):
    """docstring for Document"""
    def __init__(self, arg):
        super(Document, self).__init__()
        self.arg = arg
        self.modified = True

    def contentsChanged(self):
        pass

    def isModified(self):
        return self.modified

    def setModified(self):
        pass


class Projekt(QGroupBox,QModelIndex):
    """This is the projekt class"""
    sequenceNumber = 1

    def __init__(self):
        super(Projekt, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # I must change all 'document' class reference to 'project' class… so I need to enhance project with modify flags and signals
        self.document = Document('unknown')
        # Create a new project
        self.project = projekt.new_project()
        # Create a new output
        the_out = self.project.new_output('OSC')

        # initialize selection (this might be done with models later)
        self.scenario_selected = None
        self.event_selected = None
        self.output_selected = None

        # Create Project Attributes layout
        self.createProjectAttrGroupBox()
        # Create Scenario List layout
        self.createScenarioListGroupBox()
        # Create Scenario Attributes layout
        self.createScenarioAttrGroupBox()

        # Create the main layout
        mainLayout = QGridLayout()
        # Integrate the layout previously created
        mainLayout.addWidget(self.project_Groupbox, 0, 0, 1, 2)
        mainLayout.addWidget(self.ScenarioListGroupBox, 2, 0)
        mainLayout.addWidget(self.ScenarioAttrGroupBox, 2, 1)
        # Make the main layout strechable when resizing main window
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        # Integrate main layout to the main window
        self.setLayout(mainLayout)
    
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

    def newFile(self):
        """create a new project"""
        self.isUntitled = True
        self.curFile = "project %d" % Projekt.sequenceNumber
        Projekt.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.project.name = self.curFile
        if not self.project.path:
            self.project_path.setText('Project has not been saved')      
        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        """open an existing project file"""
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # read a project and create scenario
        self.project.read(fileName)
        self.outputs_refresh()
        self.scenario_list_refresh()
        self.project_display()
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        #self.document().contentsChanged.connect(self.documentWasModified)
        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False
        else:
            fileName = fileName + '.json'
        return self.saveFile(fileName)

    def saveFile(self, fileName=None):
        """ save project"""
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if fileName:
            self.project.write(fileName)
            self.project_path.setText(fileName)
        else:
            self.project.write()
            self.project_path.setText(self.project.path)
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        return True

    def openFolder(self):
        """ open project directory"""
        if self.project.path:
            directory, filename = os.path.split(self.project.path)
            from subprocess import call
            call(["open", directory])
            return True
        else:
            False

    def project_display(self):
        self.project_author.setText(self.project.author)
        self.project_version.setText(self.project.version)
        self.project_path.setText(self.project.path)

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.document.isModified():
            ret = QMessageBox.warning(self, "MDI",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        #self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).baseName()
  
    def scenario_list_orderChanged(self,event):
        """appelé à chaque modif d'ordre"""
        item = self.scenario_list.currentItem()
        x = self.scenario_list.row(item)
        QListWidget.dropEvent(self.scenario_list, event)
        y = self.scenario_list.row(item)
        self.project.scenarios_set(x,y)

    def scenarioSelectionChanged(self,current,previous):
        if current:
            index = self.scenario_list.row(current)
            if self.project.scenarios() != []:
                self.scenario_selected = self.project.scenarios()[index]
            else:
                self.scenario_selected = None    
        else:
            if previous:
                if self.scenario_list.currentRow() >= 0:
                    index = self.scenario_list.row(previous)
                    if self.project.scenarios() != []:
                        self.scenario_selected = self.project.scenarios()[index]
                    else:
                        self.scenario_selected = None    
                else:
                    self.scenario_selected = None
            else:
                self.scenario_selected = None
        if not self.scenario_selected:
            self.scenario_display_clear()
            self.scenario_del.setDisabled(True)
            self.scenario_play.setDisabled(True)
            self.scenario_output_index.setDisabled(True)
            self.scenario_output_protocol.setDisabled(True)
            self.scenario_description.setDisabled(True)
            self.scenario_content.setDisabled(True)
        else:
            self.scenario_display(self.scenario_selected)
            self.scenario_del.setDisabled(False)
            self.scenario_play.setDisabled(False)
            self.scenario_output_index.setDisabled(False)
            self.scenario_output_protocol.setDisabled(False)
            self.scenario_description.setDisabled(False)
            self.scenario_content.setDisabled(False)

    def newScenario(self):
        scenario = self.project.new_scenario()
        item = QListWidgetItem(scenario.name)
        self.scenario_list.addItem(item)
        self.scenario_list.setCurrentItem(item)

    def delScenario(self):
        if self.scenario_selected:
            scenar2delete = self.scenario_selected
            # Remove the item from the QlistWidget
            self.scenario_list.takeItem(self.scenario_list.row(self.scenario_list.currentItem()))
            # and then delete the scenario object
            self.project.del_scenario(scenar2delete)

    def playScenario(self):
        self.scenario_selected.play()

    def scenario_list_refresh(self):
        self.scenario_list.clear()
        for scenario in self.project.scenarios():
            scenario = QListWidgetItem(scenario.name)
            scenario.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
            self.scenario_list.addItem(scenario)
        self.scenario_list.show()

    def scenario_display_clear(self):
        self.scenario_content.clear()
        self.scenario_output_index.clear()
        self.scenario_output_protocol.clear()
        self.scenario_output_text.clear()
        self.scenario_description.clear()

    def scenario_out_display(self,scenario):
        self.scenario_output_protocol.clear()
        protocols = []
        for protocol in self.project.getprotocols():
            if not protocol in protocols:
                protocols.append(protocol)
        for protocol in protocols:
            self.scenario_output_protocol.addItem(protocol)
        out = self.scenario_selected.getoutput()
        if out:
            self.scenario_output_text.setText(out.ip+':'+str(out.udp)+' ('+out.name+')')
        else:
            print 'no outputs available'

    def scenario_display(self,scenario):
        self.scenario_display_clear()
        self.scenario_out_display(scenario)
        if scenario.output:
            out_protocol = scenario.output[0]
            out_index = scenario.output[1]
            self.scenario_output_index.setValue(scenario.output[1])
            self.scenario_output_protocol.setCurrentIndex(self.scenario_output_protocol.findText(scenario.output[0]))
        else:
            if self.project.outputs() == []:
                self.scenario_output_text.setText('No available output')
                self.scenario_output_protocol.setDisabled(True)
                self.scenario_output_index.setDisabled(True)
        self.scenario_description.setText(scenario.description)
        if scenario.events() != []:
            for event in scenario.events():
                line = event.content
                #not really nice…
                if isinstance(line,unicode):
                    line = projekt.unicode2string_list(line)
                if isinstance(line,int):
                    line = str(line)
                else:
                    line = str(line)
                    line = ''.join( c for c in line if  c not in "[]'," )
                line = QListWidgetItem(line)
                line.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
                self.scenario_content.addItem(line)
        else:
            empty = QListWidgetItem()
            empty.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
            self.scenario_content.addItem(empty)

    def event_delete(self):
        if self.event_selected:
            # check if it's not the last line
            if self.scenario_content.row(self.scenario_content.currentItem()) != len(self.scenario_selected.events()):
                event2delete = self.event_selected
                self.scenario_content.takeItem(self.scenario_content.row(self.scenario_content.currentItem()))
                self.scenario_selected.del_event(event2delete)
            else:
                # We need to check if 
                print 'AH'
                #self.scenario_display_clear()
                #self.scenario_display(self.scenario_selected)
                #self.event_selected = None

    def event_right_click(self,QPos):
        self.listMenu= QMenu()
        play = self.listMenu.addAction("Play Event")
        play_from_here = self.listMenu.addAction("Play From Here")
        play.triggered.connect(self.event_play_func)
        play_from_here.triggered.connect(self.event_play_from_here_func)
        parentPosition = self.scenario_content.mapToGlobal(QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show() 

    def event_play_func(self):
        if self.event_selected and type(self.event_selected.content) != int:
            self.event_selected.play()

    def event_play_from_here_func(self):
        if self.event_selected:
            self.scenario_selected.play_from_here(self.event_selected)

    def scenario_name_changed(self):
        self.scenario_selected.name = self.scenario_list.currentItem().text()
        self.scenario_list_refresh()

    def scenario_description_changed(self):
        self.scenario_selected.description = self.scenario_description.text()

    def scenario_output_index_changed(self):
        self.scenario_selected.output[1] = self.scenario_output_index.value()
        self.scenario_out_display(self.scenario_selected)

    def scenario_output_protocol_changed(self):
        protocol = self.scenario_output_protocol.currentText()
        protocol = protocol.encode('utf-8')
        if protocol:
            length = len(self.project.outputs(protocol))
            self.scenario_output_index.setRange(1,length)
            self.scenario_output_index.setDisabled(False)
            if not self.scenario_selected.output:
                # current scenario has no output, so we will create it
                self.scenario_selected.output = [None,None]
                self.scenario_selected.output[0] = protocol
                if len(self.scenario_selected.output) == 1:
                    self.scenario_selected.output.append(1)
                else:
                    self.scenario_selected.output[1] = 1
                self.scenario_output_index.setValue(1)

    def scenario_content_changed(self):
        # check if there is some text
        if self.scenario_content.currentItem().text():
            newline = self.scenario_content.currentItem().text()
            if isinstance(newline, unicode):
                newline = newline.encode('utf-8')
            newline = newline.split(' ')
            newline = projekt.unicode2_list(newline)
            if isinstance(newline,float):
                newline = int(newline)
                self.scenario_content.currentItem().setText(str(newline))
            # check if newline is int (wait) or not
            if type(newline) == int:
                pass
            # if we have a list as arguments, we need to keep a list
            elif len(newline) > 1:
                newline = [newline[0],newline[1:]]
            # if it's a new line (the last line), append line to content attr of Scenario class and create a new Event instance
            if self.scenario_content.currentRow() + 1 == self.scenario_content.count():
                new_event = self.scenario_selected.new_event(content=newline)
                empty = QListWidgetItem()
                empty.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
                self.scenario_content.addItem(empty)
                self.event_play.setDisabled(False)
                self.event_del.setDisabled(False)
                self.event_selected = new_event
            else:
                self.scenario_selected.events()[self.scenario_content.currentRow()].content = newline

    def eventSelectionChanged(self):
        if self.scenario_selected:
            if self.scenario_content.currentRow() >= 0 and self.scenario_content.currentRow() < len(self.scenario_selected.events()):
                item = self.scenario_content.currentRow()
                item = self.scenario_selected.events()[item]
                self.event_selected = item
            else:
                self.event_selected = None
        else:
            self.event_selected = None
        if self.event_selected:
            self.event_del.setDisabled(False)
            if type(self.event_selected.content) != int:
                self.event_play.setDisabled(False)
            else:
                self.event_play.setDisabled(True)
        else:
            self.event_del.setDisabled(True)
            self.event_play.setDisabled(True)

    def project_author_changed(self):
        self.project.author = self.project_author.text()

    def project_version_changed(self):
        self.project.version = self.project_version.text()
