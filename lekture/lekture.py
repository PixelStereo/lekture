#!/usr/bin/env python
import os
import json
import random
from time import sleep
from time import time
import socket

import lekture
import devicemanager
import lekture_events as events
import lekture_devices as devices


debug = True

extension = '.json'
projectpath = os.path.abspath(os.path.dirname(__file__))
projectpath = projectpath + '/projects/'

project = {}
devices_db = {'osc_device': {'port':1234,'ip':'127.0.0.1'}}
application_db = {'data':{},'attributes':{'name':'lekture','author':'Pixel Stereo','version':'0.0.1'}}
#project.setdefault('events',events.db)
project.setdefault('application',application_db)
project.setdefault('devices',devices.db)

#devicemanager.run(11111)

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

def read(path='') : 
    if not os.path.exists(path):
        print "ERROR - THIS PATH IS NOT VALuid" , path
    else :
        try:
            with open(path) as in_file :
                if debug : print 'file reading : ' , path
                loaded = json.load(in_file,object_hook=unicode2string_dict)
                in_file.close()
                for key,val in loaded.items():
                    if key == 'events' :
                        events.db.clear()
                        for k,v in loaded['events'].items():
                            events.db.setdefault(k,v)  
                        """create an instance of the Event class 
                        for each event in the project loaded"""
                        for event in events.db['data'].keys():
                            uid = event
                            name = events.db['data'][event]['attributes']['name']
                            output = events.db['data'][event]['attributes']['output']
                            description = events.db['data'][event]['attributes']['description']
                            event_content = events.db['data'][event]['attributes']['content']
                            events.new(uid=uid,name=name,description=description,output=output,event_content=event_content)
                    elif key == 'application' :
                        """need to create an application class"""
                        application_db.clear()
                        for k,v in loaded['events'].items():
                            events.db.setdefault(k,v)  
                if debug : print 'project loaded'
                if debug : print 'events.db : ' , events.db
                if debug : print 'application_db : ' , application_db
        except IOError:
            if debug : print 'error : project not loaded'

def write(file_path='') :
    if file_path == '':
        file_path = projectpath + "test.json"
    out_file = open(str(file_path), 'w')
    out_file.write(json.dumps(project,ensure_ascii=True,separators=(',', ': ')))
    out_file.close()
    if debug : print ("file has been written : " , file_path)

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
    print 'CALLLLLL'
    if debug :  'content' , content
    for event in content:
        event = event.split(" ",1)
        toto.setdefault(event[0],event[1:])
    toto = lekture.unicode2string_dict(toto)
    return toto


