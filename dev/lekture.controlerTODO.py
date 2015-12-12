    selecta = ''
    timepoint_selecta = '0'


    @pyqtSlot()
    def on_event_timepoint_delete_clicked(self):
        """delete a timepoint in the selected event"""
        selection = self.timepoint_selecta
        self.timepoint_selecta = None
        self.event_content.clear()
        self.cur_obj().timepoint_delete(selection)
        self.event_timepoints_refresh()

    def event_timepoints_refresh(self):
        """list all timepoints"""
        self.event_timepoints_model.clear()
        timepoints = events['data'][self.selecta]['attributes']['content'].keys()
        if timepoints:
            timepoints = sorted(timepoints)
            #self.event_timepoints_model.setCurrentIndex(timepoints[0])
            for timepoint in timepoints:
                item = QStandardItem(timepoint)
                self.event_timepoints_model.appendRow(item)
        
    @pyqtSlot("QAbstractItemModel")
    def on_event_timepoints_model_dataChanged(self,index):
        print 'ZONB' , index

    @pyqtSlot("QModelIndex")
    def on_event_timepoints_clicked(self,index):
        """an event has been selected from UI"""
        if debug : print "TIMEPOINTS selected" , index.row(), index.data()
        print self.event_timepoints_model
        #print self.event_timepoints_model.itemFromIndex(index)
        item = index.data()
        #item = item.encode("utf8")
        self.timepoint_selecta = item
        self.event_content_refresh()
    
    def event_content_refresh(self):
        item = self.timepoint_selecta
        content = events['data'][self.selecta]['attributes']['content'][item]
        self.event_content.clear()
        for key,val in content.items():
            self.event_content.addItem(key + " " + str(val))      

    @pyqtSlot("QModelIndex")
    def on_events_list_clicked(self,index):
        """a event has been selected from UI"""
        if debug : print "selected event" , index.row(), index.data()
        myselection = index.data()
        if myselection != '':
            #myselection = myselection.encode('ascii', 'ignore')
            self.selecta = myselection
            if debug : print 'selection triggered frol the UI' , self.selecta
            toto = events['data'][self.selecta]['attributes']
            self.event_description.setText(toto['description'])
            self.event_name.setText(toto['name'])
            self.event_output.setText(toto['output'])
            #for key,value in events[selection]['attributes']['content']:
            #content_string = lekture.dict2string(events[selection]['attributes']['content'])
            #self.event_content.insert(content_string)
            self.event_timepoints_refresh()
            self.event_group.show()
        else :
            self.event_group.hide()

    @pyqtSlot()
    def on_event_delete_clicked(self):
        """delete an event"""
        self.cur_obj().delete()
        self.events_list_refresh()
        self.selecta = ''
        self.event_group.hide()

    @pyqtSlot()
    def events_list_refresh(self):
        """ refresh events list UI"""
        self.events_model.clear()
        for key in events['data'].keys():
            item = QStandardItem(key)
            self.events_model.appendRow(item)
        #events_list = lekture.events.listing()
        #print events_list
        #for event in events_list:
        #    self.events_list.addItem(event)
        # if no selection, no need to display event attributes
        #if self.selection != '' : 
        #    self.event_group.show()
        #else :
        #    self.event_group.hide()


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """ open project"""
        file_path = self.file_open_select()
        if debug : print 'file_path OPEN REQUEST' , file_path
        lekture.read(file_path)
        self.events_list_refresh()

    @pyqtSlot()
    def on_osc_server_active_stateChanged(self):
        state = self.osc_server_active.checkState()
        print state




