#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QDialog,QMenu,QToolBar
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox,QTableWidget

# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../PyProjekt')
sys.path.append(projekt_path)

# import projekt
from lek_projekt import Projekt
# import outputs panel
from outputs import OutputsPanel

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
        
        self.child = None

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()
        self.setWindowTitle("LEKTURE")

        mytoolbar = QToolBar() 
        #self.toolbar = self.addToolBar()
        mytoolbar.addAction(self.newAct)
        mytoolbar.addAction(self.openAct)
        mytoolbar.addAction(self.saveAct)
        mytoolbar.addAction(self.saveAsAct)
        mytoolbar.addAction(self.outputsAct)
        self.addToolBar( Qt.LeftToolBarArea , mytoolbar )

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
        self.child = child

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
        self.outputsAct.setEnabled(hasProjekt)
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
        self.child = child
        return child

    def createActions(self):
        self.newAct = QAction("&New", self,
                shortcut=QKeySequence.New, statusTip="Create a new file",
                triggered=self.newFile)

        self.openAct = QAction("&Open...", self,
                shortcut=QKeySequence.Open, statusTip="Open an existing file",
                triggered=self.open)

        self.saveAct = QAction("&Save", self,
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

        self.outputsAct = QAction("Outputs", self,
                statusTip="Open the outputs panel",
                triggered=self.openOutputsPanel)

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

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openFolderAct)
        self.fileMenu.addAction(self.exitAct)

        self.OutputsMenu = self.menuBar().addMenu("&Outputs")
        self.OutputsMenu.addAction(self.outputsAct)
        self.OutputsMenu.setDisabled(True)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Pixel Stereo', 'lekture')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(1000, 650))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('Pixel Stereo', 'lekture')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeProjekt(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            self.OutputsMenu.setDisabled(False)
            return activeSubWindow.widget()
        else:
            self.OutputsMenu.setDisabled(True)
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

    def openOutputsPanel(self):
        if self.child:
            #project = self.mdiArea.currentSubWindow()
            project = self.activeProjekt().project
            pos = self.pos()
            size = self.size()
            output_panel = OutputsPanel(project,pos,self.activeProjekt())

