#!/usr/bin/env python
"""import os
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
from lekture_functions import timestamp as timestamp"""

from functions import timestamp
from functions import unicode2string_dict
from projects import Project 
from projects import Event

debug=0

# this is not the best way to do.
#But if i don't do that, I can't create events objects 
# because when I call Event.getinstances(), the instances list is empty
event_list = []

debug = True

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

def getprojectpath():
    return projectpath


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


