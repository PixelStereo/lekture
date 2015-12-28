#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QMenu
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox

# for development of pyprojekt, use git version
import os,sys
lib_path = os.path.abspath('./../PyProjekt')
sys.path.append(lib_path)

from pyprojekt import projekt

debug = True
projekt.debug = True
projekt.test = False


class MainWindow(QMainWindow):
    """This create the main window of the application"""
    def __init__(self):
        super(MainWindow, self).__init__()

        # remove close & maximize window buttons
        #self.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowMinimizeButtonHint)
        self.setMinimumSize(850,450)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)

        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        
        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()
        self.setWindowTitle("LEKTURE")


    def closeEvent(self, scenario):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            scenario.ignore()
        else:
            self.writeSettings()
            scenario.accept()

    def newFile(self):
        child = self.createProjekt()
        child.newFile()
        child.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findProjekt(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createProjekt()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.activeProjekt() and self.activeProjekt().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeProjekt() and self.activeProjekt().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def openFolder(self):
        if self.activeProjekt() and self.activeProjekt().openFolder():
            self.statusBar().showMessage("File revealed in Finder", 2000)

    def about(self):
        QMessageBox.about(self, "About MDI",
                "<b>Lekture</b> is an OSC sequencer "
                "This release is an alpha version. Don't use it in production !!")

    def updateMenus(self):
        hasProjekt = (self.activeProjekt() is not None)
        self.saveAct.setEnabled(hasProjekt)
        self.saveAsAct.setEnabled(hasProjekt)
        self.openFolderAct.setEnabled(hasProjekt)
        self.closeAct.setEnabled(hasProjekt)
        self.closeAllAct.setEnabled(hasProjekt)
        self.nextAct.setEnabled(hasProjekt)
        self.previousAct.setEnabled(hasProjekt)
        self.separatorAct.setVisible(hasProjekt)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeProjekt())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createProjekt(self):
        child = Projekt()
        self.mdiArea.addSubWindow(child)
        return child

    def createActions(self):
        self.newAct = QAction(QIcon(':/images/new.png'), "&New", self,
                shortcut=QKeySequence.New, statusTip="Create a new file",
                triggered=self.newFile)

        self.openAct = QAction(QIcon(':/images/open.png'), "&Open...", self,
                shortcut=QKeySequence.Open, statusTip="Open an existing file",
                triggered=self.open)

        self.saveAct = QAction(QIcon(':/images/save.png'), "&Save", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.openFolderAct = QAction("Open Project Folder" ,self,
                statusTip="Reveal Project in Finder",triggered=self.openFolder)

        self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)

        self.closeAct = QAction("Cl&ose", self,
                statusTip="Close the active window",
                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,
                statusTip="Close all the windows",
                triggered=self.mdiArea.closeAllSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                shortcut=QKeySequence.PreviousChild,
                statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openFolderAct)
        self.fileMenu.addAction(self.exitAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Pixel Stereo', 'lekture')
        pos = settings.value('pos', QPoint(200, 200))
        #size = settings.value('size', QSize(400, 400))
        self.move(pos)
        #self.resize(size)

    def writeSettings(self):
        settings = QSettings('Pixel Stereo', 'lekture')
        settings.setValue('pos', self.pos())
        #settings.setValue('size', self.size())

    def activeProjekt(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findProjekt(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)


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
        self.project = projekt.new_project()
        self.scenario_selected = None
        self.event_selected = None
        self.output_selected = None

        self.createProjectAttrGroupBox()
        self.createOuputAttrGroupBox()
        self.createScenarioListGroupBox()
        self.createScenarioAttrGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.project_Groupbox, 0, 0, 1, 2)
        mainLayout.addWidget(self.outputs_GroupBox, 1, 0, 1, 2)
        mainLayout.addWidget(self.ScenarioListGroupBox, 2, 0)
        mainLayout.addWidget(self.ScenarioAttrGroupBox, 2, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
    
    def createProjectAttrGroupBox(self):
        self.project_Groupbox = QGroupBox('Project')
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

        project_layout.addWidget(project_author_label)
        project_layout.addWidget(project_author)
        project_layout.addWidget(project_version_label)
        project_layout.addWidget(project_version)
        project_layout.addWidget(project_path_label)
        project_layout.addWidget(project_path)
        project_layout.addStretch(1)
        self.project_Groupbox.setLayout(project_layout)   

    def createOuputAttrGroupBox(self):
        self.outputs_GroupBox = QGroupBox("Outputs")
        output_protocol_label = QLabel('Protocol')
        output_protocol = QComboBox()
        output_protocol.addItem("OSC")
        output_protocol.addItem("Artnet")
        output_protocol.addItem("MIDI")
        output_protocol.addItem("Serial")
        output_selector_label = QLabel('Output')
        output_selector = QSpinBox()
        output_selector.setMinimumSize(50,20)
        output_ip_label = QLabel('IP address')
        output_ip = QLineEdit()
        output_udp_label = QLabel('UDP port')
        output_udp = QSpinBox()
        output_udp.setRange(0,65536)
        output_name_label = QLabel('name')
        output_name = QLineEdit()
        output_new = QPushButton('New Output')

        self.output_selector = output_selector
        self.output_udp = output_udp
        self.output_ip = output_ip
        self.output_protocol = output_protocol
        self.output_name = output_name
        self.output_new = output_new

        self.output_selector.valueChanged.connect(self.output_selector_changed)
        output_selector.setValue(1)
        output_selector.setRange(1,len(self.project.outputs()))
        
        self.output_new.released.connect(self.output_new_func)
        self.output_name.textEdited.connect(self.output_name_changed)
        self.output_protocol.currentIndexChanged.connect(self.output_protocol_changed)
        self.output_ip.textEdited.connect(self.output_ip_changed)
        self.output_udp.valueChanged.connect(self.output_udp_changed)

        output_layout = QHBoxLayout()
        output_layout.addWidget(output_new)
        output_layout.addWidget(output_protocol_label)
        output_layout.addWidget(output_protocol)
        output_layout.addWidget(output_selector_label)
        output_layout.addWidget(output_selector)
        output_layout.addWidget(output_ip_label)
        output_layout.addWidget(output_ip)
        output_layout.addWidget(output_udp_label)
        output_layout.addWidget(output_udp)
        output_layout.addWidget(output_name_label)
        output_layout.addWidget(output_name)
        output_layout.addStretch(1)
        self.outputs_GroupBox.setLayout(output_layout)   

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

    def project_display(self):
        self.project_author.setText(self.project.author)
        self.project_version.setText(self.project.version)
        self.project_path.setText(self.project.path)

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
        else:
            self.project.write()
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

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeScenario(self, scenario):
        if self.maybeSave():
            scenario.accept()
        else:
            scenario.ignore()

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
        self.scenario_list.setMinimumSize(120,290)
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
        layout.setRowStretch(2, 1)
        layout.setColumnStretch(0, 1)
        self.ScenarioListGroupBox.setLayout(layout)    

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
            self.scenario_output.setDisabled(True)
            self.scenario_description.setDisabled(True)
            self.scenario_content.setDisabled(True)
        else:
            self.scenario_display(self.scenario_selected)
            self.scenario_del.setDisabled(False)
            self.scenario_play.setDisabled(False)
            self.scenario_output.setDisabled(False)
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
        self.scenario_output.clear()
        self.scenario_description.clear()
        self.scenario_output_text.clear()

    def scenario_out_display(self,scenario):
        out = self.project.outputs()[scenario.output-1]
        self.scenario_output_text.setText(out.ip+':'+str(out.udp)+' ('+out.name+')')

    def scenario_display(self,scenario):
        self.scenario_display_clear()
        self.scenario_output.setValue(scenario.output)
        self.scenario_description.setText(scenario.description)
        self.scenario_out_display(scenario)
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

    def createScenarioAttrGroupBox(self):
        self.ScenarioAttrGroupBox = QGroupBox("Scenario Content")
        # Assign an output to the seleted scenario
        self.scenario_output_label = QLabel('output')
        self.scenario_output = QSpinBox()
        self.scenario_output.setMinimumSize(50,20)
        self.scenario_output.setDisabled(True)
        self.scenario_output.setRange(1,len(self.project.outputs()))
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

        self.scenario_output.valueChanged.connect(self.scenario_output_changed)
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
        layout.setRowStretch(8, 1)
        self.ScenarioAttrGroupBox.setLayout(layout)

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

    def scenario_output_changed(self):
        self.scenario_selected.output = self.scenario_output.value()
        self.scenario_out_display(self.scenario_selected)

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
        self.scenario_output.setRange(1,len(self.project.outputs()))
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
        self.output_udp.clear()
        self.output_name.clear()
        self.output_ip.clear()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    #mainWin.setFixedSize(1000,650)
    mainWin.show()
    sys.exit(app.exec_())
