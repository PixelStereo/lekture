#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from PyQt5.QtCore import Qt,QModelIndex,QFileInfo,QFile
from PyQt5.QtWidgets import QFileDialog,QListWidgetItem,QApplication,QMessageBox,QTableWidgetItem,QSpinBox,QComboBox
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QLabel,QLineEdit,QListWidget,QAbstractItemView,QPushButton,QGridLayout

# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../../PyProjekt')
sys.path.append(projekt_path)

from pyprojekt import project
from panels import createProjectAttrGroupBox, createScenarioListGroupBox, createScenarioAttrGroupBox, createOuputAttrGroupBox
from functions import event2line, line2event

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
        self.project = project.new_project()
        # Create a new output
        the_out = self.project.new_output('OSC')

        # initialize selection (this might be done with models later)
        self.scenario_selected = None
        self.event_selected = None
        self.output_selected = None

        # this lock is used when fillin out_protocol QComboBox
        self.out_locked = False

        # Create Project Attributes layout
        createProjectAttrGroupBox(self)
        # Create Scenario List layout
        createScenarioListGroupBox(self)
        # Create Scenario Attributes layout
        createScenarioAttrGroupBox(self)
        # Create Outputs layout
        createOuputAttrGroupBox(self)
        # Integrate Both scenario_list and scenario_attr in a group
        scenario_layout = QGridLayout()
        scenario_layout.addWidget(self.ScenarioListGroupBox, 2, 0)
        scenario_layout.addWidget(self.ScenarioAttrGroupBox, 2, 1)
        scenario_layout.setRowStretch(2, 1)
        scenario_layout.setColumnStretch(0, 1)
        scenario_layout.setColumnStretch(1, 1)
        scenario_group = QGroupBox()
        scenario_group.setLayout(scenario_layout)
        self.scenario_group = scenario_group
        self.outputs_group.setVisible(False)
        self.protocol_display()

        # Create the main layout
        mainLayout = QGridLayout()
        # Integrate the layout previously created
        mainLayout.addWidget(self.project_Groupbox, 0, 0, 1, 2)
        mainLayout.addWidget(scenario_group, 1, 0)
        mainLayout.addWidget(self.outputs_group, 1, 0)
        self.mainLayout = mainLayout
        # Integrate main layout to the main window
        self.setLayout(mainLayout)

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
        #self.outputs_refresh()
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
            self.project.path = fileName
        else:
            self.project.write()
            self.project_path.setText(self.project.path)
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        return True

    def openFolder(self):
        """ open project directory"""
        if self.project.path:
            path = self.project.path
            if sys.platform == 'darwin':
                subprocess.check_call(["open", "-R", path])
            elif sys.platform == 'win32':
                subprocess.check_call(['explorer', path])
            elif sys.platform.startswith('linux'):
                subprocess.check_call(['xdg-open', '--', path])
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
        scenarios = self.project.scenarios()
        if current:
            scenar = current
        elif previous and self.scenario_list.currentRow() >= 0:
            scenar = previous
        else:
            scenar = None
        if scenar and scenarios != []:
            index = self.scenario_list.row(scenar)
            self.scenario_selected = scenarios[index]
            self.scenario_output_index_range()
            self.scenario_display(self.scenario_selected)
            self.scenario_del.setDisabled(False)
            self.scenario_play.setDisabled(False)
            self.scenario_output_index.setDisabled(False)
            self.scenario_output_protocol.setDisabled(False)
            self.scenario_description.setDisabled(False)
            self.scenario_content.setDisabled(False)
        else:
            self.scenario_selected = None    
            self.scenario_display_clear()
            self.scenario_del.setDisabled(True)
            self.scenario_play.setDisabled(True)
            self.scenario_output_index.setDisabled(True)
            self.scenario_output_protocol.setDisabled(True)
            self.scenario_description.setDisabled(True)
            self.scenario_content.setDisabled(True)

    def newScenario(self):
        scenario = self.project.new_scenario()
        item = QListWidgetItem(scenario.name)
        item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
        self.scenario_list.addItem(item)
        # The current scenario has not an output available, so assign the first one.
        # In lekture, we always have a default output (OSC), created when creating a project
        scenario.output = [None,None]
        scenario.output[0] = self.project.getprotocols()[0]
        scenario.output[1] = 1
        # setting selection will trigger scenario_display function
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

    def scenario_out_fill(self):
        scenario = self.scenario_selected
        self.out_locked = True
        self.scenario_output_protocol.clear()
        protocols = []
        for protocol in self.project.getprotocols():
            # we want to have protocol only once in the menu
            if not protocol in protocols:
                protocols.append(protocol)
        for protocol in protocols:
            self.scenario_output_protocol.addItem(protocol)
        if scenario:
            self.scenario_output_protocol.setCurrentIndex(self.scenario_output_protocol.findText(scenario.output[0]))
        self.out_locked = False

    def scenario_out_display(self,scenario):
        self.out_locked = True
        out = scenario.getoutput()
        self.scenario_output_index.setValue(scenario.output[1])
        self.scenario_output_protocol.setCurrentIndex(self.scenario_output_protocol.findText(scenario.output[0]))
        self.scenario_out_text_display()
        self.out_locked = False

    def scenario_out_text_display(self):
        scenario = self.scenario_selected
        out = scenario.getoutput()
        if out:
            if scenario.output[0] == 'OSC' or scenario.output[0] == 'PJLINK':
                self.scenario_output_text.setText(out.ip+':'+str(out.udp)+' ('+out.name+')')
            else:
                self.scenario_output_text.setText(scenario.output[0]+' protocol is not working')
        else:
            self.scenario_output_text.setText('No output')

    def scenario_display(self,scenario):
        """This function is called when scenario_selected changed"""
        self.scenario_display_clear()
        self.scenario_out_fill()
        self.scenario_out_display(scenario)
        self.scenario_description.setText(scenario.description)
        if scenario.events() != []:
            for event in scenario.events():
                line = event.content
                line = event2line(line)
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
                # If it's the last line, we don't delete the last line
                pass
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
        # We set a lock when fillin the menu
        if not self.out_locked:
            if self.scenario_selected:
                self.scenario_selected.output[1] = self.scenario_output_index.value()
                self.scenario_out_text_display()

    def scenario_output_protocol_changed(self):
        # We set a lock when fillin the menu
        if not self.out_locked:
            protocol = self.scenario_output_protocol.currentText()
            protocol = protocol.encode('utf-8')
            if protocol:
                # When protocol change, we set the output_index to 1
                self.scenario_output_index.setValue(1)
                # change to the new value inputed by user
                self.scenario_selected.output = [protocol,1]
                self.scenario_output_index_range()

    def scenario_output_index_range(self):
        """update range to existing outputs of this protocol"""
        if self.scenario_selected:
            length = len(self.project.outputs(self.scenario_selected.output[0]))
        else:
            length = None
        if length:
            self.scenario_output_index.setRange(1,length)
            self.scenario_output_index.setDisabled(False)
        else:
            self.scenario_output_index.setRange(0,0)
            self.scenario_output_index.setDisabled(True)

    def scenario_content_changed(self):
        # check if there is some text
        item = self.scenario_content.currentItem().text()
        if item:
            newline = line2event(self,item)
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
        if self.scenario_selected and self.scenario_content.currentRow() >= 0 and self.scenario_content.currentRow() < len(self.scenario_selected.events()):
            item = self.scenario_content.currentRow()
            item = self.scenario_selected.events()[item]
            self.event_selected = item
            self.event_del.setDisabled(False)
            if type(self.event_selected.content) != int:
                self.event_play.setDisabled(False)
            else:
                self.event_play.setDisabled(True)
        else:
            self.event_selected = None
            self.event_del.setDisabled(True)
            self.event_play.setDisabled(True)

    def project_author_changed(self):
        self.project.author = self.project_author.text()

    def project_version_changed(self):
        self.project.version = self.project_version.text()

    def new_output_func(self):
        protocol = self.protocol.currentText()
        self.project.new_output(protocol)
        self.protocol_display()

    def protocol_display(self):
        self.protocol_table.clear()
        # we know there is at least one protocol in lekture, OSC is create when creating a project
        protocol = self.protocol.currentText()
        self.protocol_table.setRowCount(len(self.project.outputs(protocol)))
        row = 0
        for out in self.project.outputs(protocol):
            col = 0
            attrs = out.vars_()
            for attr in attrs:
                if attr.startswith('_'):
                    attrs.remove(attr)
            attrs.sort()
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
