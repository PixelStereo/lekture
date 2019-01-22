#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main window handles :
- main window
- Menus and all documents-related functions
such as new / open / save / save as…
"""


import os
import sys

import pylekture

from projekt import Projekt

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QSignalMapper, QPoint, QSize, QSettings, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QWidget, \
                            QApplication, QMessageBox, QFileDialog


class MainWindow(QMainWindow):
    """
    The main window of the application
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # remove close & maximize window buttons
        #self.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowMinimizeButtonHint)
        self.setMinimumSize(500, 666)
        #self.setMaximumSize(1000,666)
        self.project_widget = QWidget()
        # revamp
        #self.project_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #self.project_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.project_widget)

        self.project = None
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
        mytoolbar.addSeparator()
        mytoolbar.addAction(self.outputsAct)
        mytoolbar.addAction(self.scenarioAct)
        self.scenarioAct.setVisible(False)
        mytoolbar.setMovable(False)
        mytoolbar.setFixedWidth(60)
        self.addToolBar(Qt.LeftToolBarArea, mytoolbar)

    def closeEvent(self, scenario):
        """
        method called when the main window wants to be closed
        """
        self.project_widget.close()
        self.writeSettings()
        scenario.accept()

    def newFile(self):
        """creates a new project"""
        project = self.createProjekt()
        project.newFile()
        project.show()
        self.project = project

    def open(self):
        """open a project"""
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            project = self.createProjekt()
            if project.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                project.show()
            else:
                project.close()

    def save(self):
        """
        called when user save a project
        """
        if self.project and self.project.save():
            self.statusBar().showMessage("File saved", 2000)
        else:
            self.statusBar().showMessage("Error when trying to save the file")

    def saveAs(self):
        """called when user save AS a project"""
        if self.project and self.project.saveAs():
            self.statusBar().showMessage("File saved", 2000)
        else:
            self.statusBar().showMessage("Error when trying to save the file")

    def openFolder(self):
        """called when user calls 'reveal in finder' function"""
        if self.project and self.project.openFolder():
            self.statusBar().showMessage("File revealed in Finder", 2000)

    def about(self):
        """called when user wants to know a bit more on the app"""
        import sys
        python_version = str(sys.version_info[0])
        python_version_temp = sys.version_info[1:5]
        for item in python_version_temp:
            python_version = python_version + "." + str(item)
        QMessageBox.about(self, "About Lekture",
                            "pylekture build " + str(pylekture.__version__ + "\n" + \
                            "python version " + str(python_version)))

    def updateMenus(self):
        """update menus"""
        hasProjekt = (self.project is not None)
        self.saveAct.setEnabled(hasProjekt)
        self.saveAsAct.setEnabled(hasProjekt)
        self.outputsAct.setEnabled(hasProjekt)
        self.scenarioAct.setEnabled(hasProjekt)
        self.openFolderAct.setEnabled(hasProjekt)
        self.closeAct.setEnabled(hasProjekt)
        self.separatorAct.setVisible(hasProjekt)

    def updateWindowMenu(self):
        """unpates menus on the window toolbar"""
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.separatorAct)

    def createProjekt(self):
        """create a new project"""
        project = Projekt()
        self.project_widget(project)
        self.project = project
        return project

    def createActions(self):
        """create all actions"""
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

        self.openFolderAct = QAction("Open Project Folder", self,
                                     statusTip="Reveal Project in Finder",
                                     triggered=self.openFolder)

        self.closeAct = QAction("Cl&ose", self,
                                statusTip="Close the active window",
                                triggered=self.project_widget.close)

        self.outputsAct = QAction("Outputs", self,
                                  statusTip="Open the outputs panel",
                                  triggered=self.openOutputsPanel)

        self.scenarioAct = QAction("Scenario", self,
                                   statusTip="Open the scenario panel",
                                   triggered=self.openScenarioPanel)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

    def createMenus(self):
        """create all menus"""
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openFolderAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.outputsAct)
        self.viewMenu.addAction(self.scenarioAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createStatusBar(self):
        """create the status bar"""
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        """read the settings"""
        settings = QSettings('Pixel Stereo', 'lekture')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(1000, 650))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        """write settings"""
        settings = QSettings('Pixel Stereo', 'lekture')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())


    def findProjekt(self, fileName):
        """return the project"""
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.project_widget.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def openOutputsPanel(self):
        """switch to the outputs editor"""
        if self.child:
            self.project.scenario_events_group.setVisible(False)
            self.project.outputs_group.setVisible(True)
            self.scenarioAct.setVisible(True)
            self.outputsAct.setVisible(False)

    def openScenarioPanel(self):
        """
        switch to the scenario editors
        """
        if self.child:
            self.project.scenario_events_group.setVisible(True)
            self.scenarioAct.setVisible(False)
            self.outputsAct.setVisible(True)
