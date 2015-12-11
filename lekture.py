#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from PyQt5.QtCore import pyqtSlot , QDir , QAbstractListModel , Qt , QModelIndex,QObject,QItemSelectionModel
from PyQt5.uic import loadUiType,loadUi
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QWidget,QApplication,QHBoxLayout,QDialog,QListView,QListWidget,QTableWidget,QTableView,QFileDialog,QTableWidgetItem,QWidget,QTreeView,QMainWindow,QPushButton 
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import  QStandardItemModel , QStandardItem

from span import span

#devices = span.devices.db
#events = span.events.db
application = span.application_db

debug = True
span.debug = False
span.events.debug = False

def debugUI(whatitis , WHAT2PRINT = ''):
    if debug : print "TRIGGERED FROM UI : " + whatitis , WHAT2PRINT

# LOAD THE UI FILE GENERATED BY QT CREATOR / DESIGNER
form_class, base_class = loadUiType('lekture.ui')

model_obj = {}

class spanUI(QMainWindow, form_class):
    """create span view and controller (MVC)"""
    def __init__(self):
        super(spanUI, self).__init__()
        self.setupUi(self)
        # load a style sheet
        self.setStyleSheet(open("style.qss", "r").read())
        #read a project
        path = span.projectpath+'test.json'
        span.read(path=path)
        # make a model with span file
        self.span_model = QStandardItemModel()
        # get part of the span project
        pages = span.getpages()
        for page in pages:
            model = QStandardItem(page)
            self.span_model.appendRow(model)
            model_obj.setdefault(page,{'model':model})
            if page == 'events':
                # add events
                for event in span.events.db['data']:
                    self.add_event_to_model(event)

        # Load span model in page view (diplay the main parts of the project)
        self.pageview.setModel(self.span_model)
        self.span_tree_view.setModel(self.span_model)
        # make a model of the view selection
        self.page_selection = self.pageview.selectionModel()
        self.span_tree_view.setSelectionModel(self.page_selection)
        # page selection changed
        self.page_selection.selectionChanged.connect(self.page_selected)
        #self.page_selection.select(model_obj['events']['model'].index())

        # connect events_list (list of events) to the qlistview in UI
        self.events_list.setModel(self.span_model)
        self.events_list.setRootIndex(model_obj['events']['model'].index())
        self.event_selection = self.events_list.selectionModel()
        self.event_selection.selectionChanged.connect(self.event_selected)

        """
        self.span_model.dataChanged.connect(self.edit)

 
        # 
        item = model_obj['events']['model'].index()
        item = item.child(0,0)
        self.event_display(item)
        #CREATE NAME SELECTION
        self.name_selection = self.event_name.selectionModel()
        self.name_selection.selectionChanged.connect(self.name_selected)
        #CREATE DESCRIPTION SELECTION
        self.description_selection = self.event_description.selectionModel()
        self.description_selection.selectionChanged.connect(self.description_selected)
        #CREATE OUTPUT SELECTION
        self.output_selection = self.event_output.selectionModel()
        self.output_selection.selectionChanged.connect(self.output_selected)"""

    selecta = ''

    @pyqtSlot("QItemSelection")
    def page_selected(self, data):
        """wait for a QItemSelection to send the current interface to display"""
        pass
        for selection in data.indexes():
            selection = self.absolutePath(selection)
            self.selection = selection.encode('utf-8')
            if debug:print('PAGE_SELECTION' , self.selection)
            if self.selection == '[events]':
                self.events_group.show()
            else:
                self.events_group.hide()

    @pyqtSlot()
    def on_event_new_clicked(self):
        """ make a new event"""
        key = span.events.new()
        self.add_event_to_model(key)

    def cur_obj(self):
        cur_obj = span.events.objects[self.selecta]
        return cur_obj

    @pyqtSlot()
    def on_event_timepoint_new_clicked(self):
        """create a timepoint in the selected event"""
        key = self.cur_obj().timepoint_new()
        self.add_timepoint_to_event(key)

    @pyqtSlot()
    def on_event_timepoint_delete_clicked(self):
        """delete a timepoint in the selected event"""
        key = self.cur_obj().timepoint_delete(self)
        self.del_timepoint_in_event(key)

    def add_event_to_model(self,event):
        # create the event model
        event_model = QStandardItem(event)
        # add the event model to the dict
        model_obj['events'].setdefault(event,{'model':event_model})
        # get the events page model from the dict
        events_model = model_obj['events']['model']
        # add the current event to the events page model
        events_model.appendRow(event_model)
        # get attributes of the event
        attributes = span.events.db['data'][event]['attributes'].keys()
        for attribute in attributes:
            data = span.events.db['data'][event]['attributes'][attribute]
            attribute_model = QStandardItem(attribute)
            event_model.appendRow(attribute_model)
            model_obj['events'][event].setdefault(attribute,{'model':attribute_model})
            if type(data) == dict:
                #if we have a dict, we split each element (it is timepoints and commands)
                for timepoint in data.keys():
                    timepoint_model = QStandardItem(timepoint)
                    attribute_model.appendRow(timepoint_model)
                    model_obj['events'][event][attribute].setdefault(timepoint,{'model':timepoint_model})
                    for command,value in data[timepoint].items():
                        command = command+ ' ' + str(value)
                        command_model = QStandardItem(command)
                        timepoint_model.appendRow(command_model)
                        model_obj['events'][event]['content'][timepoint].setdefault(command,command_model)
            else:
                attribute_model.appendRow(QStandardItem(data))

    def add_timepoint_to_event(self,timepoint):
        print 'TIMEPOINT TO ADD TO EVENT' , timepoint
        event = self.selecta
        print 'EVENT WHERE TO ADD THE TIMEPOINT' , event
        timepoint_model = QStandardItem(timepoint)
        model_obj['events'][event]['content']['model'].appendRow(timepoint_model)

    def del_timepoint_in_event(self,timepoint):
        print 'TIMEPOINT TO DEL IN EVENT' , timepoint
        event = self.selecta
        print 'EVENT WHERE TO DEL THE TIMEPOINT' , event
        #timepoint_model = QStandardItem(timepoint)
        model_obj['events'][event]['content']['model'].removeRow(timepoint)

    @pyqtSlot("QItemSelection")
    def event_selected(self, data):
        """an event is selected"""
        item = data.indexes()[0]
        self.selecta = item.data()
        self.event_display(item)
        item=item.data()
        self.selecta = item.encode('utf-8')
        if debug:print 'EVENT SELECTION' , self.selecta

    def event_display(self,event):
        """create a model for a view of an event with timepoints merged as 'wait' commands"""
        # connect event attributes       
        self.event_name.setModel(self.span_model)
        self.event_output.setModel(self.span_model)
        self.event_description.setModel(self.span_model)
        self.event_timepoints.setModel(self.span_model)
        self.event_timepoint_content.setModel(self.span_model)
        #create the selection for this event_timepoints
        self.timepoint_selection = self.event_timepoints.selectionModel()
        self.timepoint_selection.selectionChanged.connect(self.timepoint_selectioned)
        output = event.child(1,0)
        name = event.child(2,0)
        description = event.child(3,0)
        timepoints = event.child(0,0)
        commands = event.child(0,0).child(0,0)
        self.event_output.setRootIndex(output)
        self.event_name.setRootIndex(name)
        self.event_description.setRootIndex(description)
        self.event_timepoints.setRootIndex(timepoints)
        self.event_timepoint_content.setRootIndex(commands)
 


        #create the model for this view
        event_model = QStandardItemModel()
        event_model.dataChanged.connect(self.edit_event)
        self.event_content.setModel(event_model)
        #create the selection for this view
        self.commands_selection = self.event_content.selectionModel()
        self.commands_selection.selectionChanged.connect(self.commands_selectioned)
        #get the event uid 
        event = event.data()
        event = event.encode('utf-8')
        #get the content of the event
        event = span.events.db['data'][event]
        #get the timepoints of this event
        timepoints = event['attributes']['content'].keys()
        timepoints = sorted(timepoints)
        for timepoint in timepoints:
            #record the timepoint
            q_timepoint = QStandardItem(timepoint)
            event_model.appendRow(q_timepoint)
            #record the associated commands to this timepoint
            for command,value in event['attributes']['content'][timepoint].items():
                q_command = QStandardItem(command+str(value))
                event_model.appendRow(q_command)

    @pyqtSlot("QItemSelection")
    def timepoint_selectioned(self, data):
        """a timepoint is selected"""
        the_QModelindex = data.indexes()
        item = the_QModelindex[0]
        item = self.absolutePath(item)
        self.selection = item#.encode('utf-8')
        if debug:print('TIMEPOINT SELECTION' , self.selection)
    
    @pyqtSlot("QItemSelection")
    def commands_selectioned(self,data):
        data=data.indexes()[0].data()
        print 'COMMANDS SELECTION' , data
        self.command_selected = data

    @pyqtSlot("QItemSelection")
    def edit_event(self,data):
        """edit content of an event and record 'wait' as timepoints"""
        data = data.data()
        data = data.encode('utf-8')
        if self.command_selected.isdigit():
            print 'IN EVENT',self.selecta,'REMOVE TIMEPOINT', self.command_selected,'NEW TIMEPOIINT',data
        else:
            print 'IN EVENT',self.selecta,'OLD COMMAND' , self.command_selected,'NEW COMMAND',data

    @pyqtSlot("QItemSelection")
    def content_selected(self, data):
        the_QModelindex = data.indexes()
        item = the_QModelindex[0]
        item = self.absolutePath(item)
        if type(item) == list:
            ilist = []
            for i in item:
                i = i.encode('utf-8')
                ilist.append(i)
            self.selection = ilist
        else:
            self.selection = item#.encode('utf-8')
        if debug:print('SELECTION' , self.selection)

    @pyqtSlot("QItemSelection")
    def name_selected(self, data):
        the_QModelindex = data.indexes()
        item = the_QModelindex[0]
        item = self.absolutePath(item)
        self.selection = item#.encode('utf-8')
        if debug:print('SELECTION' , self.selection)

    @pyqtSlot("QItemSelection")
    def description_selected(self, data):
        the_QModelindex = data.indexes()
        item = the_QModelindex[0]
        item = self.absolutePath(item)
        self.selection = item#.encode('utf-8')
        if debug:print('SELECTION' , self.selection)

    @pyqtSlot("QItemSelection")
    def output_selected(self, data):
        the_QModelindex = data.indexes()
        item = the_QModelindex[0]
        item = self.absolutePath(item)
        self.selection = item#.encode('utf-8')
        if debug:print('SELECTION' , self.selection)

    def absolutePath(self,item):
        """accept a QModelIndex and a value and write into span dictionary (in span.py file)"""
        isparent = item.parent()
        path = [item.data()]
        if isparent.isValid():
            path.insert(0,isparent.data().encode('utf-8'))
            isparent = isparent.parent()
            if isparent.isValid():
                path.insert(0,isparent.data())
                isparent = isparent.parent()                
                if isparent.isValid():
                    path.insert(0,isparent.data())
                    isparent = isparent.parent()                
                    if isparent.isValid():
                        path.insert(0,isparent.data())
        #path.insert(0,'[')
        #path.append(']')
        if len(path) == 1:
            path =  '['+path[0]+ ']'
        elif len(path) == 2:
            path =   '['+path[0]+ '][data]['+path[1]+']'
        elif len(path) == 3:
            path = '['+path[0]+ '][data]['+path[1]+']['+path[2]+']'
        elif len(path) == 4:
            path = '['+path[0]+ '][data]['+path[1]+'][attributes]['+path[2]+']['+path[3]+']'
        #path = ']['.join(path)
        #path = '['+path+']'
        return path

    @pyqtSlot("QItemSelection")
    def edit(self, data):
        #address = self.selection.encode('utf-8')
        #address =  address[0]
        #print address
        #print span.project + address
        print "DATA CHANGED :"  , self.selection , (data.data())
        print "PLEASE HELP TO DO THIS"

    @pyqtSlot()
    def on_actionNew_triggered(self):
        """Create a new project (reload everything)"""
        self.span_model.clear()
        debugUI("NEW PROJECT")
        self.__init__()
        debugUI("RELOAD SPAN")

    @pyqtSlot()
    def on_actionOpenDir_triggered(self):
        """ open project directory"""
        file_path = span.getprojectpath()
        directory, filename = os.path.split(file_path)
        from subprocess import call
        call(["open", directory])
        debugUI("OPEN DIRECTORY")

    @pyqtSlot()
    def on_actionSave_triggered(self):
        """ save project"""
        debugUI('SAVE PROJECT')
        span.write()

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        """save project as"""
        file_path = self.file_saveas_select()
        debugUI("SAVE PROJECT AS")
        span.write(file_path)

    def file_open_select(self):
        """choose file dialog window"""
        file_path = QFileDialog().getOpenFileName(self, "Select a Span project to open",)
        if file_path:
            if debug : print 'file_path has been selected' , file_path
            file_path = file_path[0]
            span.file_path = file_path
            self.events_list_refresh()
            return file_path

    def file_saveas_select(self):
        """choose file dialog window"""
        file_path = QFileDialog.getSaveFileName(self, "Save span project")
        if debug : print "SAVE AS" , file_path
        if file_path:
            file_path = file_path[0]
            #self.file_pathUI.setText(file_path)
            return file_path
    
    @pyqtSlot()
    def on_event_play_clicked(self):
        """ an event is playing"""
        if debug : print 'PLAY'
        self.cur_obj().play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = spanUI()
    appWindow.move(5,12)
    appWindow.show()
    sys.exit(app.exec_())
    sdRef.close()
