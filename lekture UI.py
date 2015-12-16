#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtCore import QStringListModel , QSettings , QSize ,QPoint , QSignalMapper ,QObject,QFile,QFileInfo,QTextStream
from PyQt5.QtCore import pyqtSlot , QDir , QAbstractListModel , Qt , QModelIndex,QItemSelectionModel,QDateTime,QTimer
from PyQt5.uic import loadUiType,loadUi
from PyQt5.QtWidgets import QAction ,QWidget,QApplication,QHBoxLayout,QDialog,QListView,QListWidget,QTableWidget,QFormLayout,QRadioButton,QCheckBox,QGridLayout,QLabel,QSizePolicy,QTextEdit,QSpinBox,QSlider,QDial
from PyQt5.QtWidgets import QTableView,QFileDialog,QTableWidgetItem,QTreeView,QMainWindow,QPushButton , QGroupBox,QMdiArea,QTabWidget,QMessageBox,QVBoxLayout,QComboBox,QStyleFactory,QLineEdit,QDateTimeEdit,QScrollBar
from PyQt5.QtGui import  QStandardItemModel , QStandardItem , QIcon , QKeySequence


from lekture import lekture

debug = True
lekture.debug = True

def debugUI(whatitis , WHAT2PRINT = ''):
    if debug : print "TRIGGERED FROM UI : " + whatitis , WHAT2PRINT

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

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

        self.setWindowTitle("MDI")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def newFile(self):
        child = self.createMdiChild()
        child.newFile()
        child.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def about(self):
        QMessageBox.about(self, "About MDI",
                "The <b>MDI</b> example demonstrates how to write multiple "
                "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

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
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createMdiChild(self):
        child = MdiChild()
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
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)





    """ PROJECT FILE MANAGEMENT """

    def new_project(self):
        """method used for ProjectNew and ProjectOpen"""
        self.project_model.clear()
        child = Project_Window()
        child.newFile()
        child.show()
        

    def save_as_project(self,path):
        debugUI("SAVE PROJECT AS")
        self.project.path = path+'.json'
        self.project.write()

    def open_project(self,path):
        if path:
            debugUI('OPEN PROJECT')
            self.project.path = path
            self.new_project()
            self.project.read()
        else:
            debugUI('OPEN CANCELLED')


    @pyqtSlot()
    def on_ProjectNew_triggered(self):
        """Create a new project (reload everything)"""
        debugUI("NEW PROJECT")
        self.new_project()

    @pyqtSlot()
    def on_ProjectOpen_triggered(self):
        """open a project (reload everything)"""
        debugUI("OPEN PROJECT")
        path = QFileDialog().getOpenFileName(self, "Select a lekture project to open",)
        path = path[0]
        if os.path.exists(path):
            self.open_project(path)
        else:
            debugUI('OPEN CANCELLED')

    @pyqtSlot()
    def on_ProjectSave_triggered(self):
        """ save project"""
        debugUI('SAVE PROJECT')
        if os.path.exists(self.project.path):
            self.project.write()
        else:
            self.save_as_project()

    @pyqtSlot()
    def on_ProjectSave_as_triggered(self):
        """save project as"""
        debugUI("SAVE AS")
        path = QFileDialog.getSaveFileName(self, "Save lekture project")
        if path:
            path = path[0]
        if os.path.exists(path):
            self.save_as_project(path)
        else:
            debugUI('SAVE_AS CANCELLED')
    
    @pyqtSlot()
    def on_ProjectOpenDir_triggered(self):
        """ open project directory"""
        debugUI("OPEN DIRECTORY")
        directory, filename = os.path.split(self.project.path)
        from subprocess import call
        call(["open", directory])



class Document(object):
    """docstring for Document"""
    def __init__(self, arg):
        super(Document, self).__init__()
        self.arg = arg

    def contentsChanged(self):
        pass

    def isModified(self):
        pass

    def setModified(self):
        pass

        



class MdiChild(QGroupBox):
    sequenceNumber = 1

    def __init__(self):
        super(MdiChild, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # I must change all document reference to project… so I need to enhance project with modify flags and signals
        self.document = Document('unknown')
        self.project = lekture.Project()
        print 'PROJECT-UI' , self.project

        self.originalPalette = QApplication.palette()


        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createRightGroupBox()
        self.createBottomLeftTabWidget()

        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.RightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)

        topLayout = QHBoxLayout()
        project_author_label = QLabel('author')
        project_author = QLineEdit(self.project.author)
        project_version_label = QLabel('version')
        project_version = QLineEdit(self.project.version)
        project_path_label = QLabel('path')
        project_path = QLineEdit(self.project.path)
        project_path.setFixedWidth(600)
        topLayout.addWidget(project_author_label)
        topLayout.addWidget(project_author)
        topLayout.addWidget(project_version_label)
        topLayout.addWidget(project_version)
        topLayout.addWidget(project_path_label)
        topLayout.addWidget(project_path)
        topLayout.addStretch(1)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.RightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        
        #QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setStyle(QStyleFactory.create('Macintosh'))
        #QApplication.setStyle(QStyleFactory.create('Windows'))
        QApplication.setPalette(QApplication.style().standardPalette())



    def newFile(self):
        self.isUntitled = True
        self.curFile = "project %d" % MdiChild.sequenceNumber
        MdiChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.project.path = fileName
        self.events_list_refresh()
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

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

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
        return QFileInfo(fullFileName).fileName()




    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Events List")
        self.events_list = QListWidget()
        self.events_list.itemSelectionChanged.connect(self.eventSelectionChanged)
        self.event_new = QPushButton(('New Event'))
        self.event_new.released.connect(self.newEvent)

        layout = QVBoxLayout()
        layout.addWidget(self.event_new)
        layout.addWidget(self.events_list)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def eventSelectionChanged(self):
		items = self.events_list.selectedItems()
		x=[]
		for i in list(items):
			x.append(str(i.text()))
		print x[0]

    def newEvent(self):
    	event = self.project.new_event()
        self.events_list_refresh()

    def events_list_refresh(self):
        self.events_list.clear()
        print self.project.events()
        for event in self.project.events():
            self.events_list.addItem(str(event))

    def createRightGroupBox(self):
        self.RightGroupBox = QGroupBox("Event Content")
        self.RightGroupBox.setCheckable(True)
        self.RightGroupBox.setChecked(True)

        self.event_name_label = QLabel('name')
        self.event_name = QLineEdit()
        self.event_output_label = QLabel('output')
        self.event_output = QLineEdit()
        self.event_description_label = QLabel('description')
        self.event_description = QLineEdit()
        self.event_content_label = QLabel('content')
        self.event_content = QListWidget()

        layout = QGridLayout()

        layout.addWidget(self.event_name_label, 0, 0)
        layout.addWidget(self.event_name, 0, 1)
        layout.addWidget(self.event_output_label, 0, 2)
        layout.addWidget(self.event_output, 0, 3, 1, 2)
        layout.addWidget(self.event_description_label, 1, 0)
        layout.addWidget(self.event_description, 1, 1)
        layout.addWidget(self.event_content_label, 2, 0)
        layout.addWidget(self.event_content, 2, 1, 2, 2)
        layout.setRowStretch(5, 1)
        self.RightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.setFixedSize(1000,550)
    mainWin.move(0,0)
    mainWin.show()
    sys.exit(app.exec_())
