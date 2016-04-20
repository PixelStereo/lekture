#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Child module hosts a project-related class
A Projekt class is created for each sub-window / project.
A Projekt handles scenario and outputs
"""

from pylekture import project
from pylekture.functions import checkType, prop_list
from panels import create_panels

import sys
import subprocess
from PyQt5.QtCore import Qt, QModelIndex, QFileInfo, QFile, QPoint, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QApplication, QMenu, \
                            QMessageBox, QTableWidgetItem, QGroupBox, QGridLayout, \
                            QComboBox


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
        if not self.project:
            print('ERROR 123 - pylekture cannot create a project')
            sys.exit(1)
        # Create a new output
        the_out = self.project.new_output('OSC')
        # initialize selection (this might be done with models later)
        self.scenario_selected = None
        # the event in the scenario content
        self.event_selected = None
        # the event in the project's events bin
        self.event_list_selected = None
        # the output
        self.output_selected = None
        # this lock is used when fillin out_protocol QComboBox
        self.out_locked = False
        # create all panels
        create_panels(self)

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
        #self.document().commandsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        """
        Open an existing project file
        """
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            flag = True
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # read a project and create scenario
        if self.project.read(fileName):
            #self.outputs_refresh()
            self.table_list_refresh('scenario')
            self.table_list_refresh('event')
            self.project_display()
            self.protocol_display()
            QApplication.restoreOverrideCursor()
            self.setCurrentFile(fileName)
            flag = False
        else:
            flag = True
        if flag:
            QMessageBox.warning(self, "Lekture Error 123",
                                "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        #self.document().commandsChanged.connect(self.documentWasModified)
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
        return self.saveFile(fileName)

    def saveFile(self, fileName=None):
        """
        save project (called after save and saveas method)
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if fileName:
            answer = self.project.write(fileName)
            self.project_path.setText(fileName)
            self.project.path = fileName
        else:
            answer = self.project.write()
            self.project_path.setText(self.project.path)
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        return answer

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
        #self.project_version.setText(self.project.version)
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
            ret = QMessageBox.warning(self, "your project",
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
            self.scenario_description.setDisabled(True)
            self.scenario_content.setDisabled(True)
            #self.scenario_events_group.setVisible(False)
        if scenar:
            index = self.scenario_list.row(scenar)
            self.scenario_selected = scenarios[index]
            self.scenario_display(self.scenario_selected)
            self.scenario_del.setDisabled(False)
            self.scenario_play.setDisabled(False)
            self.scenario_description.setDisabled(False)
            self.scenario_content.setDisabled(False)
            #self.scenario_events_group.setVisible(True)

    def new_scenario(self):
        """
        Create a new scenario
        """
        scenario = self.project.new_scenario()
        # If output = None, it will use the project outputs.
        # In lekture, we always have a default output (OSC), created when creating a project
        self.table_list_refresh('scenario')
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
            self.table_list_refresh('scenario')
            if self.scenario_list.rowCount() <= row:
                row = self.scenario_list.rowCount() - 1
            self.scenario_list.setCurrentCell(row, 0)

    def playScenario(self):
        """
        Play the selected scenario
        """
        self.scenario_selected.play()

    def table_list_refresh(self, ttype='scenario'):
        """
        Refresh scenario/events table view
        """
        if ttype == 'scenario':
            widget_table = self.scenario_list
            widget_table.clearContents()
            items = self.project.scenarios
            header = self.scenario_list_header
        elif ttype == 'event':
            widget_table = self.events_list_table
            widget_table.clearContents()
            items = self.project.events
            header = self.events_list_header
        else:
            return False
        widget_table.setRowCount(len(items))
        for item in items:
            for column in header:
                index = items.index(item)
                if column == 'output':
                    value = getattr(item, column)
                    menu = QComboBox()
                    output = self.output_list_refresh(item, menu)
                    widget_table.setCellWidget(index, header.index(column), menu)
                    menu.currentIndexChanged.connect(self.scenario_list.signalMapper.map)
                    self.scenario_list.signalMapper.setMapping(menu, menu)
                    # we can use a ComboBox in a table without selecting the current row.
                    # so we have to pass to the signalMapper the scenario object
                    menu.item = item
                else:
                    if column == 'duration':
                        value = item.getduration()
                        widg = QTableWidgetItem(str(value))
                        widg.setFlags(Qt.NoItemFlags)
                        widg.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
                    elif column == 'command':
                        value = self.line_to_command(item.command)
                        widg = QTableWidgetItem(str(value))
                        widg.setFlags(Qt.NoItemFlags)
                        widg.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
                    else:
                        value = getattr(item, column)
                        widg = QTableWidgetItem(str(value))
                        widg.setFlags(Qt.NoItemFlags)
                        widg.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable)
                    widget_table.setItem(index, header.index(column), widg)

    @pyqtSlot(QComboBox)
    def output_changed(self, menu):
        """
        output has changed from events_list table or scenario_list table
        """
        if menu.currentIndex() == 0:
            # this is the 'parent' value. 
            menu.item._output = None
        else:
            index = menu.currentIndex() - 1
            menu.item.output = self.project.outputs[index]

    def scenario_display_clear(self):
        """
        clear the scenario table view
        """
        self.scenario_content.clear()
        self.scenario_output_text.clear()
        self.scenario_description.clear()

    def scenario_out_display(self, scenario):
        """
        Display a readable output description
        """
        out = scenario.output
        if out:
            if scenario.output.service == 'OutputUdp':
                output_string = out.ip + ':' + str(out.udp) + ' ('+out.name+')'
            elif scenario.output.service == 'OutputMidi':
                output_string = 'port : ' + out.port + ' ('+out.name+')'
            else:
                output_string = scenario.output.service + ' protocol is not working'
            self.scenario_output_text.setText(output_string)
        else:
            self.scenario_output_text.setText('No output')

    def line_to_command(self, line):
        if isinstance(line, list):
            the_string = ''
            for item in line:
                the_string = the_string + str(item) + ' '
                line = the_string
        elif isinstance(line, int):
            line = str(line)
        return line


    def scenario_display(self, scenario):
        """
        This function is called when scenario_selected changed
        """
        # first, clear the scenario_display
        self.scenario_display_clear()
        # display a nice string to explain which is the default output for the whole scenario
        self.scenario_out_display(scenario)
        # display the description of the scenario
        self.scenario_description.setText(scenario.description)
        if scenario.events != []:
            # scenario contains events
            for event in scenario.events:
                line = event.command
                line = self.line_to_command(line)
                line = QListWidgetItem(line)
                line.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|\
                              Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
                self.scenario_content.addItem(line)
        # add an empty item at the end.
        # It will be used to create a new event, just typing into it.
        empty = QListWidgetItem()
        empty.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable|\
                       Qt.ItemIsSelectable|Qt.ItemIsDragEnabled)
        self.scenario_content.addItem(empty)

    def event_delete(self):
        """
        Delete the selected event (event in the scenario content)
        """
        if self.event_selected:
            # check if it's not the last line
            cot = self.scenario_content.currentItem()
            if self.scenario_content.row(cot) != len(self.scenario_selected.events):
                event2delete = self.event_selected
                # remove it from the view
                self.scenario_content.takeItem(self.scenario_content.row(cot))
                # remove it from the model
                self.scenario_selected.del_event(event2delete)
            else:
                # If it's the last line, we don't delete the last line
                pass
                #self.scenario_display_clear()
                #self.scenario_display(self.scenario_selected)
                #self.event_selected = None

    def delete_event_list(self):
        """
        Delete the event_list_selected (event in the project content)
        """
        if self.event_list_selected:
            cot = self.events_list_table.currentItem()
            event2delete = self.event_list_selected
            # remove it from the model
            if self.project.del_event(event2delete):
                # if the model answer ok to delete the event continue...
                # ...and remove it from the view
                self.events_list_table.removeRow(self.events_list_table.row(cot))

    def event_right_click(self, QPos):
        """
        Called when user right-click on an event
        """
        self.listMenu = QMenu()
        play = self.listMenu.addAction("Play one")
        play_from_here = self.listMenu.addAction("Play from here")
        play.triggered.connect(self.event_play_func)
        play_from_here.triggered.connect(self.event_play_from_here_func)
        parentPosition = self.scenario_content.mapToGlobal(QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def event_play_func(self):
        """
        Play the selected event
        """
        if self.event_selected and type(self.event_selected.command) != int:
            return self.event_selected.play()
        else:
            return False

    def event_play_from_here_func(self):
        """
        Play from the selected event
        """
        if self.event_selected:
            self.scenario_selected.play_from_here(self.event_selected)

    def play_event_list(self):
        """
        Play the selected event from the events list of the project
        """
        if self.event_list_selected and isinstance(self.event_list_selected.command, int) == False:
            return self.event_list_selected.play()
        else:
            return False

    def scenario_data_changed(self, row, col):
        """
        Scenario is edited
        """
        if  self.scenario_list.currentItem():
            try:
                data = self.scenario_list.currentItem().text()
                if self.scenario_list_header[col] == 'name':
                    self.scenario_selected.name = data
                elif self.scenario_list_header[col] == 'description':
                    self.scenario_selected.description = data
                elif self.scenario_list_header[col] == 'wait':
                    self.scenario_selected.wait = int(data)
                elif self.scenario_list_header[col] == 'loop':
                    self.scenario_selected.loop = data
                elif self.scenario_list_header[col] == 'post_wait':
                    self.scenario_selected.post_wait = int(data)
                selection = self.project.scenarios.index(self.scenario_selected)
                self.table_list_refresh('scenario')
                self.scenario_list.setCurrentCell(selection, 0)
            except:
                selection = self.project.scenarios.index(self.scenario_selected)
                self.table_list_refresh('scenario')
                self.scenario_list.setCurrentCell(selection, 0)

    def event_data_changed(self, row, col):
        """
        Event is edited in the Event Bin
        """
        if  self.events_list_table.currentItem():
            data = self.events_list_table.currentItem().text()
            if self.events_list_header[col] == 'name':
                self.event_list_selected.name = data
            elif self.events_list_header[col] == 'description':
                self.event_list_selected.description = data
            elif self.events_list_header[col] == 'command':
                data = data.split(' ')
                self.event_list_selected.command = data
            elif self.events_list_header[col] == 'wait':
                self.event_list_selected.wait = int(data)
            elif self.events_list_header[col] == 'loop':
                self.event_list_selected.loop = data
            elif self.events_list_header[col] == 'post_wait':
                self.event_list_selected.post_wait = int(data)
            # refresh the table to be sure that there is no an error
            self.table_list_refresh('event')

    def scenario_description_changed(self):
        """
        Description of the scenario changed
        """
        self.scenario_selected.description = self.scenario_description.text()

    def output_list_refresh(self, item, menu):
        """
        Refresh the output list for a given project / scenario / event
        And returns 

        :param item: The scenario or event item we want to know the output
        :type item: a valid Scenario or Instance object
        :param menu: The name of the QComboBox object
        :type menu: a valid QComboBox object
        :returns: (int) The index of the current output
        """
        menu.clear()
        index = None
        menu.addItem('parent')
        for output in self.project.outputs:
            menu.addItem(output.name)
            if output == item.output:
                index = self.project.outputs.index(output)
        return index

    def scenario_output_changed(self):
        """
        Output index of the scenario changed
        """
        # We set a lock when fillin the menu
        if not self.out_locked:
            if self.scenario_selected:
                self.scenario_out_display(self.scenario.selected)

    def scenario_content_changed(self):
        """
        Edit the content (events) of the selected scenario
        """
        # check if there is some text
        if self.scenario_content.currentItem():
            newline = self.scenario_content.currentItem().text()
            if newline != '':
                newline = newline.split(' ')
                # there is new text on the last line
                if self.scenario_content.currentRow() + 1 == self.scenario_content.count():
                    # create a new event
                    new_event = self.new_event('Osc', newline)
                    # add the event to the scenario
                    self.scenario_selected.add_event(new_event)
                    # display the current scenario (refresh)
                    self.scenario_display(self.scenario_selected)
                else:
                    self.scenario_selected.events[self.scenario_content.currentRow()].command = newline
        # we need to refresh the duration item on the scenrio_table
        #don't understant why but with this line, the name is changed too… weird
        #item = self.scenario_list.item(self.scenario_list.currentRow(),1)
        row = self.scenario_list.currentRow()
        #duration = str(self.scenario_selected.getduration())
        #item.setText(duration)
        self.table_list_refresh('scenario')
        self.scenario_list.setCurrentCell(row, 0)

    def new_event(self, protocol='Osc', command=None):
        """
        Create a new event
        """
        new_event = self.project.new_event(protocol, command=command)
        self.table_list_refresh('event')
        return new_event

    def new_event_list(self, protocol='Osc', command=None):
        """
        Create a new event on the project's events bin
        """
        protocol = self.event_list_service.currentText()
        event = self.new_event(protocol, command)
        last = len(self.project.events)-1
        self.events_list_table.setCurrentCell(last, 0)
        self.events_list_table.setFocus()

    def eventSelectionChanged(self):
        """
        Selected event in the scenario's events list has changed
        """
        if self.scenario_selected and self.scenario_content.currentRow() >= 0 \
            and self.scenario_content.currentRow() < len(self.scenario_selected.events):
            item = self.scenario_content.currentRow()
            item = self.scenario_selected.events[item]
            self.event_selected = item
            self.event_del.setDisabled(False)
            if self.event_selected.service != 'Wait':
                self.event_play.setDisabled(False)
            else:
                self.event_play.setDisabled(True)
        else:
            self.event_selected = None
            self.event_del.setDisabled(True)
            self.event_play.setDisabled(True)

    def event_list_selection_changed(self):
        """
        Selected event in the project's bin has changed
        """
        if self.events_list_table.currentRow() >= 0 and \
           self.events_list_table.currentRow() < len(self.project.events):
            item = self.events_list_table.currentRow()
            item = self.project.events[item]
            self.event_list_selected = item
            self.event_list_del.setDisabled(False)
            if self.event_list_selected.service != 'Wait':
                self.event_list_play.setDisabled(False)
            else:
                self.event_list_play.setDisabled(True)
        else:
            self.event_list_selected = None
            self.event_list_del.setDisabled(True)
            self.event_list_play.setDisabled(True)

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
        self.table_list_refresh('scenario')
        self.table_list_refresh('event')
        self.protocol_display()

    def protocol_display(self):
        """
        Display outputs for the current protocol
        """
        self.protocol_table.clear()
        # we know there is at least one protocol in lekture, OSC is create when creating a project
        protocol = self.protocol.currentText()
        self.protocol_table.setRowCount(len(self.project.outputs))
        row = 0
        for out in self.project.outputs:
            col = 0
            self.protocol_table.setColumnCount(len(self.output_list_header))
            for attribute in self.output_list_header:
                if attribute in prop_list(out):
                    header = QTableWidgetItem(attribute)
                    self.protocol_table.setHorizontalHeaderItem(col, header)
                    item = QTableWidgetItem(str(getattr(out, attribute)))
                    self.protocol_table.setItem(row, col, item)
                col = col + 1
            row = row + 1

    def output_table_changed(self, row, col):
        """
        An output has been edited
        """
        if self.protocol_table.currentItem():
            protocol = self.protocol.currentText()
            outs = self.project.outputs
            out = outs[row]
            attr = self.protocol_table.horizontalHeaderItem(col).text()
            value = self.protocol_table.currentItem().text()
            # just to be sure that an int won't be encoded as a symbol
            value = checkType(value)
            setattr(out, attr, value)
            if attr == 'name':
                self.table_list_refresh('scenario')
                self.table_list_refresh('event')

    def del_output_func(self):
        if self.output_selected:
            self.project.del_output(self.output_selected)
            row = self.protocol_table.currentRow()
            self.protocol_display()
            if self.protocol_table.rowCount() <= row:
                row = self.protocol_table.rowCount() - 1
            self.protocol_table.setCurrentCell(row, 0)

    def output_selection_changed(self, current, previous):
        """
        Set output_selected variable when output selection changed
        """
        print(current, previous)
        outputs = self.project.outputs
        if current:
            output = current
        elif previous and self.protocol_table.currentRow() >= 0:
            output = previous
        else:
            output = None
            self.output_selected = None
            self.output_del.setDisabled(True)
        if output:
            index = self.protocol_table.row(output)
            self.output_selected = outputs[index]
            self.output_del.setDisabled(False)
