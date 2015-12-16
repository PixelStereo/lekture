#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions import timestamp
from functions import unicode2string_dict
from projects import Project 
from projects import Event

debug = True

project_list = []

def new_project(*args,**kwargs):
    taille = len(project_list)
    the_project = None
    project_list.append(the_project)
    project_list[taille] = Project(args,kwargs)
    return project_list[taille]









"""these funcitons are not used now… these come from my first tests without classes using a dict"""

def listdirectory2(path):  
    """list a directory"""
    projects_list = []  
    for root, dirs, files in os.walk(path):  
        for i in files:  
            projects_list.append(os.path.join(root, i))  
    return projects_list

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


