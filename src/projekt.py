#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Child module hosts a project-related class
A Projekt class is created for each sub-window / project.
A Projekt handles scenario and outputs
"""

from pylekture import project
from pylekture.functions import checkType
from panels import createProjectAttrGroupBox, createScenarioListGroupBox, \
                   createScenarioAttrGroupBox, createOuputAttrGroupBox

import sys
import subprocess
from PyQt5.QtCore import Qt, QModelIndex, QFileInfo, QFile, QPoint
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QApplication, QMenu, \
                            QMessageBox, QTableWidgetItem, QGroupBox, QGridLayout


class Document(object):
    """
    Implements a modified flag to not forget saving before quit
    """
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


class Projekt(QGroupBox, QModelIndex):
    """
    Implements pylekture project class in a dedicated sub-window
    """
    # used to create sub-windows
    sequenceNumber = 1

    def __init__(self):
        """
        Init creates the layout for a projekt
        """
        super(Projekt, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # I must change all 'document' class reference to 'project' class…
        # so I need to enhance project with modify flags and signals
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
        scenario_layout.addWidget(self.ScenarioListGroupBox, 0, 0)
        scenario_layout.addWidget(self.ScenarioAttrGroupBox, 1, 0)
        scenario_layout.setRowStretch(0, 0)
        scenario_group = QGroupBox()
        scenario_group.setLayout(scenario_layout)

        self.scenario_group = scenario_group
        self.outputs_group.setVisible(False)
        self.protocol_display()

        # Create the main layout
        mainLayout = QGridLayout()
        # Integrate the layout previously created
        self.project_Groupbox.setMaximumHeight(50)
        mainLayout.addWidget(self.project_Groupbox, 0, 0, 1, 2)
        mainLayout.addWidget(scenario_group, 1, 0)
        mainLayout.addWidget(self.outputs_group, 1, 0)
        self.mainLayout = mainLayout
        # Integrate main layout to the main window
        self.setLayout(mainLayout)

    def newFile(self):
        """
        Create a new project
        """
        self.isUntitled = True
        self.curFile = "project %d" % Projekt.sequenceNumber
        Projekt.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.project.name = self.curFile
        if not self.project.path:
            self.project_path.setText('Project has not been saved')
        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        """
        Open an existing project file
        """
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
        self.protocol_display()
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        #self.document().contentsChanged.connect(self.documentWasModified)
        return True

    def save(self):
        """
        Save a project
        """
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        """
        Save as a project
        """
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False
        else:
            fileName = fileName + '.json'
        return self.saveFile(fileName)

    def saveFile(self, fileName=None):
        """
        save project (called after save and saveas method)
        """
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
        """
        Reveal project directory in Explorer (tested on OSX only)
        """
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
            return False

    def project_display(self):
        """
        Display project's Attributes
        """
        self.project_author.setText(self.project.author)
        self.project_version.setText(self.project.version)
        self.project_path.setText(self.project.path)
        self.project_loop.setChecked(self.project.loop)
        self.project_autoplay.setChecked(self.project.autoplay)

    def userFriendlyCurrentFile(self):
        """
        Return user friendly current file name (without path)
        """
        return self.strippedName(self.curFile)

    def currentFile(self):
        """
        Return current file object
        """
        return self.curFile

    def closeEvent(self, event):
        """
        Call when project is about to be closed
        """
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        """
        Called when a modification happened on the document
        """
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        """
        Return the modified state of the project
        """
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
        """
        Set a current file
        """
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        #self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        """
        Return the stripped name of the project (without the path)
        """
        return QFileInfo(fullFileName). baseName()

    def scenarioSelectionChanged(self, current, previous):
        """
        Set scenario_selected variable when scenario selection changed
        """
        scenarios = self.project.scenarios
        if current:
            scenar = current
        elif previous and self.scenario_list.currentRow() >= 0:
            scenar = previous
        else:
            scenar = None
            self.scenario_selected = None
            self.scenario_display_clear()
            self.scenario_del.setDisabled(True)
            self.scenario_play.setDisabled(True)
            self.scenario_output_index.setDisabled(True)
            self.scenario_output_protocol.setDisabled(True)
            self.scenario_description.setDisabled(True)
            self.scenario_content.setDisabled(True)
            #self.ScenarioAttrGroupBox.setVisible(False)
        if scenar:
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
            #self.ScenarioAttrGroupBox.setVisible(True)

    def newScenario(self):
        """
        Create a new scenario
        """
        scenario = self.project.new_scenario()
        # The current scenario has not an output available, so assign the first one.
        # In lekture, we always have a default output (OSC), created when creating a project
        scenario.output = [None, None]
        scenario.output[0] = self.project.getprotocols()[0]
        scenario.output[1] = 1
        self.scenario_list_refresh()
        last = len(self.project.scenarios)-1
        self.scenario_list.setCurrentCell(last, 0)
        self.scenario_list.setFocus()

    def delScenario(self):
        """
        Delete the selected scenario
        """
        if self.scenario_selected:
            scenar2delete = self.scenario_selected
            # and then delete the scenario object
            self.project.del_scenario(scenar2delete)
            row = self.scenario_list.currentRow()
            self.scenario_list_refresh()
            if self.scenario_list.rowCount() <= row:
                row = self.scenario_list.rowCount() - 1
            self.scenario_list.setCurrentCell(row, 0)

    def playScenario(self):
        """
        Play the selected scenario
        """
        self.scenario_selected.play()

    def scenario_list_refresh(self):
        """
        Refresh scenario table view
        """
        self.scenario_list.clearContents()
        scenarios = len(self.project.scenarios)
        self.scenario_list.setRowCount(scenarios)
        for scenario in self.project.scenarios:
            index = self.project.scenarios.index(scenario)
            name_item = QTableWidgetItem(scenario.name)
            name_item.setFlags(Qt.NoItemFlags)
            name_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
            wait_item = QTableWidgetItem(str(scenario.wait))
            wait_item.setFlags(Qt.NoItemFlags)
            wait_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
            duration_item = QTableWidgetItem(str(scenario.getduration()))
            duration_item.setFlags(Qt.NoItemFlags)
            duration_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            post_wait_item = QTableWidgetItem(str(scenario.post_wait))
            post_wait_item.setFlags(Qt.NoItemFlags)
            post_wait_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
            out1_item = QTableWidgetItem(scenario.output[0])
            out1_item.setFlags(Qt.NoItemFlags)
            out1_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            out2_item = QTableWidgetItem(str(scenario.output[1]))
            out2_item.setFlags(Qt.NoItemFlags)
            out2_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
            self.scenario_list.setItem(index, 0, name_item)
            self.scenario_list.setItem(index, 1, wait_item)
            self.scenario_list.setItem(index, 2, duration_item)
            self.scenario_list.setItem(index, 3, post_wait_item)
            self.scenario_list.setItem(index, 4, out1_item)
            self.scenario_list.setItem(index, 5, out2_item)

    def scenario_display_clear(self):
        """
        clear the scenario table view
        """
        self.scenario_content.clear()
        self.scenario_output_index.clear()
        self.scenario_output_protocol.clear()
        self.scenario_output_text.clear()
        self.scenario_description.clear()

    def scenario_out_fill(self):
        """
        Fill in scenario output (in event part)
        """
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
            prot = self.scenario_output_protocol.findText(scenario.output[0])
            self.scenario_output_protocol.setCurrentIndex(prot)
        self.out_locked = False

    def scenario_out_display(self, scenario):
        """
        Display outputs for scenario
        """
        self.out_locked = True
        out = scenario.getoutput()
        self.scenario_output_index.setValue(scenario.output[1])
        prot = self.scenario_output_protocol.findText(scenario.output[0])
        self.scenario_output_protocol.setCurrentIndex(prot)
        self.scenario_out_text_display()
        self.out_locked = False

    def scenario_out_text_display(self):
        """
        Display a readable output description
        """
        scenario = self.scenario_selected
        out = scenario.getoutput()
        if out:
            if scenario.output[0] == 'OSC' or scenario.output[0] == 'PJLINK':
                self.scenario_output_text.setText(out.ip+':'+str(out.udp)+' ('+out.name+')')
            else:
                self.scenario_output_text.setText(scenario.output[0]+' protocol is not working')
        else:
            self.scenario_output_text.setText('No output')

    def scenario_display(self, scenario):
        """
        This function is called when scenario_selected changed
        """
        self.scenario_display_clear()
        self.scenario_out_fill()
        self.scenario_out_display(scenario)
        self.scenario_description.setText(scenario.description)
        # scenario contains events
        if scenario.events() != []:
            for event in scenario.events():
                line = event.content
                if isinstance(line, list):
                    the_string = ''
                    for item in line:
                        the_string = the_string + str(item) + ' '
                    line = the_string
                elif isinstance(line, int):
                    line = str(line)
                line = QListWidgetItem(line)
                line.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|\
                              Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
                self.scenario_content.addItem(line)
        empty = QListWidgetItem()
        empty.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|\
                       Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
        self.scenario_content.addItem(empty)

    def event_delete(self):
        """
        Delete the selected event
        """
        if self.event_selected:
            # check if it's not the last line
            cot = self.scenario_content.currentItem()
            if self.scenario_content.row(cot) != len(self.scenario_selected.events()):
                event2delete = self.event_selected
                self.scenario_content.takeItem(self.scenario_content.row(cot))
                self.scenario_selected.del_event(event2delete)
            else:
                # If it's the last line, we don't delete the last line
                pass
                #self.scenario_display_clear()
                #self.scenario_display(self.scenario_selected)
                #self.event_selected = None

    def event_right_click(self, QPos):
        """
        Called when user right-click on an event
        """
        self.listMenu = QMenu()
        play = self.listMenu.addAction("Play Event")
        play_from_here = self.listMenu.addAction("Play From Here")
        play.triggered.connect(self.event_play_func)
        play_from_here.triggered.connect(self.event_play_from_here_func)
        parentPosition = self.scenario_content.mapToGlobal(QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def event_play_func(self):
        """
        Play the selected event
        """
        if self.event_selected and type(self.event_selected.content) != int:
            self.event_selected.play()

    def event_play_from_here_func(self):
        """
        Play from the selected event
        """
        if self.event_selected:
            self.scenario_selected.play_from_here(self.event_selected)

    def scenario_data_changed(self, row, col):
        """
        Scenario is edited
        """
        if  self.scenario_list.currentItem():
            data = self.scenario_list.currentItem().text()
            if col == 0:
                self.scenario_selected.name = data
            elif col == 1 and data.isdigit():
                self.scenario_selected.wait = int(data)
            elif col == 2 and data.isdigit():
                self.scenario_selected.duration = int(data)
            elif col == 3 and data.isdigit():
                self.scenario_selected.post_wait = int(data)
            elif col == 4:
                self.scenario_selected.output[0] = data
            elif col == 5 and data.isdigit():
                self.scenario_selected.output[1] = int(data)
            else:
                # undo is the simplest way to do, but it's not yet implemented
                self.scenario_list_refresh()

    def scenario_description_changed(self):
        """
        Description of the scenario changed
        """
        self.scenario_selected.description = self.scenario_description.text()

    def scenario_output_index_changed(self):
        """
        Output index of the scenario changed
        """
        # We set a lock when fillin the menu
        if not self.out_locked:
            if self.scenario_selected:
                self.scenario_selected.output[1] = self.scenario_output_index.value()
                self.scenario_out_text_display()

    def scenario_output_protocol_changed(self):
        """
        Protocol for output the selected scenario has changed
        """
        # We set a lock when fillin the menu
        if not self.out_locked:
            protocol = self.scenario_output_protocol.currentText()
            protocol = protocol.encode('utf-8')
            if protocol:
                # When protocol change, we set the output_index to 1
                self.scenario_output_index.setValue(1)
                # change to the new value inputed by user
                self.scenario_selected.output = [protocol, 1]
                self.scenario_output_index_range()

    def scenario_output_index_range(self):
        """
        Update range to existing outputs of this protocol
        """
        if self.scenario_selected:
            length = len(self.project.outputs(self.scenario_selected.output[0]))
        else:
            length = None
        if length:
            self.scenario_output_index.setRange(1, length)
            self.scenario_output_index.setDisabled(False)
        else:
            self.scenario_output_index.setRange(0, 0)
            self.scenario_output_index.setDisabled(True)

    def scenario_content_changed(self):
        """
        Edit the content (events) of the selected scenario
        """
        # check if there is some text
        newline = self.scenario_content.currentItem().text()
        newline = newline.split(' ')
        # there is new text on the last line
        if self.scenario_content.currentRow() + 1 == self.scenario_content.count():
            # create a new event
            new_event = self.scenario_selected.new_event(content=newline)
            self.scenario_display(self.scenario_selected)
        else:
            self.scenario_selected.events()[self.scenario_content.currentRow()].content = newline
        # we need to refresh the duration item on the scenrio_table
        #don't understant why but with this line, the name is changed too… weird
        #item = self.scenario_list.item(self.scenario_list.currentRow(),1)
        row = self.scenario_list.currentRow()
        #duration = str(self.scenario_selected.getduration())
        #item.setText(duration)
        self.scenario_list_refresh()
        self.scenario_list.setCurrentCell(row, 0)

    def eventSelectionChanged(self):
        """
        Selected event has been changed
        """
        if self.scenario_selected and self.scenario_content.currentRow() >= 0 \
            and self.scenario_content.currentRow() < len(self.scenario_selected.events()):
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
        """
        Project author has been changed
        """
        self.project.author = self.project_author.text()

    def project_version_changed(self):
        """
        Project version has been changed
        """
        self.project.version = self.project_version.text()

    def project_autoplay_changed(self, state):
        """
        Project autoplay has been toggled
        """
        if state > 0:
            self.project.autoplay = True
        else:
            self.project.autoplay = False

    def project_loop_changed(self, state):
        """
        Project loop has been toggled
        """
        if state > 0:
            self.project.loop = True
        else:
            self.project.loop = False

    def project_play_action(self):
        """
        Play the project, button has been released
        """
        self.project.play()

    def new_output_func(self):
        """
        Create a new output for the current protocol
        """
        protocol = self.protocol.currentText()
        self.project.new_output(protocol)
        self.protocol_display()

    def protocol_display(self):
        """
        Display outputs for the current protocol
        """
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
                self.protocol_table.setHorizontalHeaderItem(col, header)
                item = QTableWidgetItem(str(getattr(out, attr)))
                self.protocol_table.setItem(row, col, item)
                col = col + 1
            row = row + 1

    def dataChanged(self, row, col):
        """
        An output has been edited
        """
        if self.protocol_table.currentItem():
            protocol = self.protocol.currentText()
            outs = self.project.outputs(protocol)
            out = outs[row]
            attr = self.protocol_table.horizontalHeaderItem(col).text()
            value = self.protocol_table.currentItem().text()
            # just to be sure that an int won't be encoded as a symbol
            value = checkType(value)
            setattr(out, attr, value)
