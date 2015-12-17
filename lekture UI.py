#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtCore import QStringListModel , QSettings , QSize ,QPoint , QSignalMapper ,QObject,QFile,QFileInfo,QTextStream
from PyQt5.QtCore import pyqtSlot , QDir , QAbstractListModel , Qt , QModelIndex,QItemSelectionModel,QDateTime,QTimer
from PyQt5.uic import loadUiType,loadUi
from PyQt5.QtWidgets import QAction ,QWidget,QApplication,QHBoxLayout,QDialog,QListView,QListWidget,QTableWidget,QFormLayout,QRadioButton,QCheckBox,QGridLayout,QLabel,QSizePolicy,QTextEdit,QSpinBox,QSlider,QDial,QListWidgetItem
from PyQt5.QtWidgets import QTableView,QFileDialog,QTableWidgetItem,QTreeView,QMainWindow,QPushButton , QGroupBox,QMdiArea,QTabWidget,QMessageBox,QVBoxLayout,QComboBox,QStyleFactory,QLineEdit,QDateTimeEdit,QScrollBar
from PyQt5.QtGui import  QStandardItemModel , QStandardItem , QIcon , QKeySequence


from lekture import lekture

debug = True
lekture.debug = True


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

        self.setWindowTitle("LEKTURE")

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

    def openFolder(self):
        if self.activeMdiChild() and self.activeMdiChild().openFolder():
            self.statusBar().showMessage("File revealed in Finder", 2000)

    def about(self):
        QMessageBox.about(self, "About MDI",
                "The <b>MDI</b> example demonstrates how to write multiple "
                "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.openFolderAct.setEnabled(hasMdiChild)
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

        

class MdiChild(QGroupBox,QModelIndex):
    sequenceNumber = 1

    def __init__(self):
        super(MdiChild, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # I must change all 'document' class reference to 'project' class… so I need to enhance project with modify flags and signals
        self.document = Document('unknown')
        self.project = lekture.new_project()
        self.events_list_selected = None

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createRightGroupBox()

        project_layout = QHBoxLayout()
        project_author_label = QLabel('author')
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

        output_layout = QHBoxLayout()
        output_selector_label = QLabel('outputs')
        output_selector = QSpinBox()
        output_ip_label = QLabel('ip address')
        output_ip = QLineEdit()
        output_udp_label = QLabel('udp port')
        output_udp = QSpinBox()
        output_udp.setRange(0,65536)
        output_name_label = QLabel('name')
        output_name = QLineEdit()

        self.output_selector = output_selector
        self.output_udp = output_udp
        self.output_ip = output_ip
        self.output_name = output_name

        self.output_selector.valueChanged.connect(self.output_selector_changed)
        output_selector.setValue(1)
        
        self.output_name.textEdited.connect(self.output_name_changed)
        self.output_ip.textEdited.connect(self.output_ip_changed)
        self.output_udp.valueChanged.connect(self.output_udp_changed)

        output_layout.addWidget(output_selector_label)
        output_layout.addWidget(output_selector)
        output_layout.addWidget(output_ip_label)
        output_layout.addWidget(output_ip)
        output_layout.addWidget(output_udp_label)
        output_layout.addWidget(output_udp)
        output_layout.addWidget(output_name_label)
        output_layout.addWidget(output_name)
        output_layout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(project_layout, 0, 0, 1, 2)
        mainLayout.addLayout(output_layout, 1, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.RightGroupBox, 2, 1)
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

        self.project.name = self.curFile
        
        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # read a project and create events
        self.project.read(fileName)
        self.events_list_refresh()
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
        file_dialog = QFileDialog(self)
        # the name filters must be a list
        file_dialog.setNameFilters(["Json Files (*.json)"])
        #file_dialog.selectNameFilter("Images (*.png *.jpg)")
        # show the dialog
        #file_dialog.exec_()
        fileName, _ = file_dialog.getSaveFileName()
        if not fileName:
            return False
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
        #return QFileInfo(fullFileName).fileName()
        return QFileInfo(fullFileName).baseName()




    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Events List")
        self.events_list = QListWidget()
        self.events_list.itemSelectionChanged.connect(self.eventSelectionChanged)
        self.event_new = QPushButton(('New Event'))
        self.event_new.released.connect(self.newEvent)
        self.event_play = QPushButton(('Play Event'))
        self.event_play.setDisabled(True)
        self.event_play.released.connect(self.playEvent)
        self.event_del = QPushButton(('Delete Event'))
        self.event_del.setDisabled(True)
        self.event_del.released.connect(self.delEvent)

        layout = QVBoxLayout()
        layout.addWidget(self.event_new)
        layout.addWidget(self.event_play)
        layout.addWidget(self.events_list)
        layout.addWidget(self.event_del)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def eventSelectionChanged(self):
        items = self.events_list.selectedItems()
        x=[]
        for i in list(items):
            x.append(str(i.text()))
        if len(x)>0:
            for event in self.project.events_obj():
                if event.uid == x[0]:
                    self.events_list_selected = event
            self.event_display(self.events_list_selected)
        else:
            self.events_list_selected = None
        if not self.events_list_selected:
            self.event_del.setDisabled(True)
            self.event_play.setDisabled(True)
        else:
            self.event_del.setDisabled(False)
            self.event_play.setDisabled(False)


    def newEvent(self):
    	event = self.project.new_event()
        self.events_list_refresh()

    def delEvent(self):
        self.project.del_event(self.events_list_selected)
        self.events_list_refresh()

    def playEvent(self):
        self.project.play_event(self.events_list_selected)

    def events_list_refresh(self):
        self.events_list.clear()
        for event in self.project.events():
            event_item = QListWidgetItem(event.uid)
            self.events_list.addItem(event_item)
        self.events_list.show()
        last = len(self.events_list)
        last = last - 1
        last = self.events_list.item(last)
        self.events_list.setCurrentItem(last)
        self.events_list.setFocus()

    def event_display(self,event):
        self.event_name.setText(event.name)
        self.event_output.setText(str(event.output))
        self.event_description.setText(event.description)
        self.event_content.clear()
        for line in event.content:
            if isinstance(line,unicode):
                line = lekture.unicode2string_list(line)
            if isinstance(line,int):
                line = str(line)
            else:
                line = str(line)
                line = ''.join( c for c in line if  c not in "[]'," )
            self.event_content.addItem(line)

    def createRightGroupBox(self):
        self.RightGroupBox = QGroupBox("Editable")
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

        self.event_name.textEdited.connect(self.event_name_changed)
        self.event_output.textEdited.connect(self.event_output_changed)
        self.event_description.textEdited.connect(self.event_description_changed)
        #self.event_content.textEdited.connect(self.event_content_changed)


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

    def event_name_changed(self):
        self.events_list_selected.name = self.event_name.text()

    def event_description_changed(self):
        self.events_list_selected.description = self.event_description.text()

    def event_output_changed(self):
        self.events_list_selected.output = self.event_output.text()

    def event_content_changed(self):
        self.events_list_selected.content = self.event_content.text()

    def output_selector_changed(self,index):
        self.output_clear()
        for output in self.project.outputs():
            if output.index == index:
                self.output_display(output)
                self.output_selected = output
            else:
                self.output_selected = None

    def output_display(self,output):
        self.output_ip.setText(output.ip)
        self.output_udp.setValue(output.udp)
        self.output_name.setText(output.name)

    def output_clear(self):
        self.output_udp.clear()
        self.output_name.clear()
        self.output_ip.clear()

    def output_name_changed(self):
        self.output_selected.name = self.output_name.text()

    def output_udp_changed(self):
        self.output_selected.udp = self.output_udp.text()

    def output_ip_changed(self):
        self.output_selected.ip = self.output_ip.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.setFixedSize(1000,550)
    mainWin.move(0,0)
    mainWin.show()
    sys.exit(app.exec_())
