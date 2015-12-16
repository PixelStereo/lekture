#!/usr/bin/env python
import os
import sys
import json
import random
import weakref
from time import sleep
import random
import devicemanager
from OSC import OSCMessage , OSCClientError
from devicemanager import OSCClient as OSCClient
client = OSCClient()
import lekture

debug=True


# this is not the best way to do.
#But if i don't do that, I can't create events objects 
# because when I call Event.getinstances(), the instances list is empty
event_list = []

debug = True

class Project(object):
    """docstring for Project"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self,*args,**kwargs):
        _new = object.__new__(self)
        Project.instances[_new] = None
        if debug :
            print
            print "........... PROJECT created ..........."
            print
        return _new

    def __init__(self, name=None,path=None,author=None,version=None):
        super(Project, self).__init__()
        # This is the extension for lekture project files
        extension = '.json'
        # During development, we use a fixed path in the repo to test
        if not name:
            name = 'temp'
        self.author = author
        self.version = version
        self.name = name
        self.path = path

    def read(self,path) : 
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print "ERROR - THIS PATH IS NOT VALID" , path
        else :
            print 'loading' , path
            try:
                with open(path) as in_file :
                    """ TODO :  FIRST WE NEED TO CLEAR THE EVENTS,DEVICES AND MODULAR APPLICATION INSTANCES"""
                    if debug : print 'file reading : ' , path
                    loaded = json.load(in_file,object_hook=lekture.unicode2string_dict)
                    in_file.close()
                    for key,val in loaded.items():
                        if key == 'events' :
                            for uid , event_dict in loaded['events']['data'].items():
                                for attribute , value in event_dict['attributes'].items():
                                    if attribute == 'content':
                                        content = value
                                    elif attribute == 'name':
                                        name = value
                                    elif attribute == 'description':
                                        description = value
                                    elif attribute == 'output':
                                        output = value
                                self.new_event(self,uid=uid,name=name,description=description,output=output,content=content)
                        elif key == 'attributes' :
                            for attribute,value in loaded['attributes'].items():
                                if attribute == 'author':
                                    self.author = value
                                if attribute == 'version':
                                    self.version = value
                                if attribute == 'name':
                                    self.name = value
                            self.lastopened = lekture.timestamp()
                    if debug : print 'project loaded'
                    self.path = path
            except IOError:
                if debug : print 'error : project not loaded'
                return False
            return True

    def write(self,path=None) :
        if path:
            savepath = path
        else:
            savepath = self.path
        out_file = open(str(savepath), 'w')
        project = {}
        project.setdefault('events',self.export_events())
        project.setdefault('attributes',self.export_attributes())
        project.setdefault('devices',{})
        out_file.write(json.dumps(project,sort_keys = True, indent = 4,ensure_ascii=False))
        if debug : print ("file has been written : " , savepath)

    def events(self):
        return Event.getinstances(self)

    def new_event(self,*args,**kwargs):
        taille = len(event_list)
        the_event = None
        event_list.append(the_event)
        event_list[taille] = Event(self)
        for key, value in kwargs.iteritems():
            setattr(event_list[taille], key, value)
        return event_list[taille]

    def play_event(self,event):
        event.play()

    def events_obj(self):
        return event_list

    def del_event(self,event):
        event_list.remove(event)

    def export_attributes(self):
        attributes = {'author':self.author,'version':self.version,'name':self.name}
        return attributes

    def export_events(self):
        events = {'data':{}}
        for event in self.events():
            events['data'].setdefault(event.uid,{'attributes':{'content':event.content,'output':event.output,'name':event.name,'description':event.description}})
        return events


class Event(Project):
    """Create a new event"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self,project,*args,**kwargs):
        _new = object.__new__(self,project)
        Event.instances[_new] = None
        if debug :
            print
            print "........... EVENT created ..........."
            print
        return _new

    def __init__(self,project='',name='',uid='',description = '',output='',content=[]):
        """create an event"""
        if output == '':
            output = '127.0.0.1:10000'
        if uid == '':
            uid = lekture.timestamp()
        if description == '':
            description = "write a comment"
        if name == '':
            name = 'untitled'
        if content == []:
            content = [['/node/string','a string'],random.randint(500,3000),['/node/integer',random.randint(65e2,65e3)],['/node/float',float(random.randint(0,100))/100],['/node/list',[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]]]            
        self.name=name
        self.project = project
        self.output=output
        self.description=description
        self.uid=uid
        self.content = content
        """if debug :
            print
            print "........... EVENT %s initing ..........." %self.name
            print
            for line in self.content:
                print 'content-line' , line
            print 'name : ' , self.name
            print 'description : ' , self.description
            print 'output : ' , self.output
            print 'uid : ' , self.uid
            print "........... EVENT %s inited ..........." %self.name
            print"""

    @staticmethod
    def getinstances(project):
        instances = []
        for event in Event.instances.keys():
            if project == event.project:
                instances.append(event)
        return instances

    # ----------- CONTENT -------------
    @property
    def content(self):
        "Current content of the event"
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @content.deleter
    def content(self):
        pass


    # ----------- NAME -------------
    @property
    def name(self):
        "Current name of the event"
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        pass

    # ----------- UID -------------
    @property
    def uid(self):
        "Current uid of the event"
        return self.__uid

    @uid.setter
    def uid(self, uid):
        self.__uid = uid

    @uid.deleter
    def uid(self):
        pass

    # ----------- DECRIPTION -------------
    @property
    def description(self):
        "Current description of the event"
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @description.deleter
    def description(self):
        pass

    # ----------- OUTPUT -------------
    @property
    def output(self):
        "Current output of the event"
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output

    @output.deleter
    def output(self):
        pass

    def play(self):
        """play an event"""
        if debug : print '------ PLAY EVENT :' , self.name , '-----------------'
        for line in self.content:
            if type(line) is int:
                if debug : print 'waiting' , line
                sleep(line/1000)
            else:
                output_ip = self.output.split(':')[0]
                output_port = self.output.split(':')[1]
                if debug : 
                    print 'todo : use bundle for each packet between wait'
                    print 'connecting to : ' + output_ip + ':' + output_port
                try:
                    client.connect((output_ip , int(output_port)))
                    msg = OSCMessage()
                    msg.setAddress(line[0])
                    msg.append(line[1])
                    client.send(msg)
                    sleep(0.01)
                    msg.clearData()
                except OSCClientError :
                    print 'Connection refused'
        return self.name , 'done'




    def delete(self):
        """delete an event"""
        del db['data'][self.uid]

    def edit(self,attr,value):
        """edit an event attribute (name,output,description,content)"""
        if debug : print (self.uid + " EDIT : " + attr + ' -> ' , value)
        del db['data'][self.uid]['attributes'][attr]
        db['data'][self.uid]['attributes'].setdefault(attr,value)