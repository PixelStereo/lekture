#!/usr/bin/env python
import os
import json
import random
#import socket
import weakref
from time import sleep
#from time import time

#import lekture
import devicemanager
import lekture_events as events
import lekture_devices as devices
from lekture_functions import timestamp as timestamp


import os, sys
lib_path = os.path.abspath('./../PyModular')
sys.path.append(lib_path)
lib_path = os.path.abspath('./PyModular')
sys.path.append(lib_path)
from modular import modular
from modular.modular import Application


#devicemanager.run(11111)



# this is not the best way to do.
#But if i don't do that, I can't create events objects 
# because when I call Event.getinstances(), the instances list is empty
event_list = []

debug = True

app = Application('lekture',author='Pixel Stereo',project='projet de test',version='0.1')

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

    def __init__(self, path=''):
        super(Project, self).__init__()
        # This is the extension for lekture project files
        extension = '.json'
        # During development, we use a fixed path in the repo to test
        if path == '':
            path = os.path.abspath(os.path.dirname(__file__))
            path = path + '/projects/'
        path = path + "test.json"
        self.path = path

    def read(self) : 
        path = self.path
        if not os.path.exists(path):
            print "ERROR - THIS PATH IS NOT VALID" , path
        else :
            try:
                with open(path) as in_file :
                    """ TODO :  FIRST WE NEED TO CLEAR THE EVENTS,DEVICES AND MODULAR APPLICATION INSTANCES"""
                    if debug : print 'file reading : ' , path
                    loaded = json.load(in_file,object_hook=unicode2string_dict)
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
                                taille = len(event_list)
                                event_list.append(uid)
                                event_list[taille] = events.Event(uid=uid,name=name,description=description,output=output,content=content)
                        elif key == 'attributes' :
                            for attribute,value in loaded['attributes'].items():
                                if attribute == 'author':
                                    self.author = value
                                if attribute == 'version':
                                    self.version = value
                                if attribute == 'project':
                                    self.project = value
                            self.lastopened = timestamp()
                    if debug : print 'project loaded'
            except IOError:
                if debug : print 'error : project not loaded'

    def write(self) :
        out_file = open(str(self.path), 'w')
        project = {}
        project.setdefault('events',events.Event.export())
        project.setdefault('application',modular.Application.export())
        """TODO : create Device Class in Modular"""
        #project.setdefault('devices',modular.Device.export())
        project.setdefault('devices',{})
        #out_file.write(json.dumps(project,ensure_ascii=True,separators=(',', ': ')))
        out_file.write(json.dumps(project,sort_keys = True, indent = 4,ensure_ascii=False))
        if debug : print ("file has been written : " , self.path)






def getpages():
    if debug : print project
    return project.keys()

def listdirectory2(path):  
    """list a directory"""
    projects_list = []  
    for root, dirs, files in os.walk(path):  
        for i in files:  
            projects_list.append(os.path.join(root, i))  
    return projects_list

def unicode2string_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = unicode2string_list(item)
        elif isinstance(item, dict):
            item = unicode2string_dict(item)
        rv.append(item)
    return rv

def getprojectpath():
    return projectpath

def unicode2string_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = unicode2string_list(value)
        elif isinstance(value, dict):
            value = unicode2string_dict(value)
        rv[key] = value
    return rv


def setdb(key,value):
    """set something in the database"""
    self.db.setdefault(key,value)
    
def getdb_value(key):
    """Request in the database"""
    self.db.get(key)

def getdb_keys(key):
    """Request in the database"""
    self.db.get(key)

def dict2string(content):
    """get event info (NEED TO BE """
    c = None
    for a , b in content.items() : 
        b = str(b)  .replace(',','').replace('\'','') + '\n'
        if c :
            c = c + a + " " + b
        else :
            c = a + " " + b
    return c

def string2dict(content):
    content = content.split('\n')
    toto = {}
    print 'CALLLL string2dict function in lekture main module'
    if debug :  'content' , content
    for event in content:
        event = event.split(" ",1)
        toto.setdefault(event[0],event[1:])
    toto = lekture.unicode2string_dict(toto)
    return toto


