#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# for development of pyprojekt, use git version
projekt_path = os.path.abspath('./../../PyProjekt')
sys.path.append(projekt_path)

from pyprojekt import functions

def event2line(line):
    if isinstance(line,unicode):
        line = functions.unicode2string_list(line)
    if isinstance(line,int):
        line = str(line)
    else:
        line = str(line)
        line = ''.join( c for c in line if  c not in "[]'," )
    return line

def line2event(self,newline):
    if isinstance(newline, unicode):
        newline = newline.encode('utf-8')
    newline = newline.split(' ')
    newline = unicode2_list(newline)
    if isinstance(newline,float):
        newline = int(newline)
        self.scenario_content.currentItem().setText(str(newline))
    # check if newline is int (wait) or not
    if type(newline) == int:
        pass
    # if we have a list as arguments, we need to keep a list
    elif type(newline) == list and len(newline) > 1:
        newline = [newline[0],newline[1:]]
    return newline

def unicode2_list(data):
    """convert unicode to list"""
    if isinstance(data,list):
        if len(data) == 1:
            rv = data[0]
            rv = functions.checkType(rv)
        else:
            rv = []
            for item in data:
                item = functions.checkType(item)
                rv.append(item)
    return rv