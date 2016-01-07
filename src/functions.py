#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyprojekt import project

def event2line(line):
    if isinstance(line,unicode):
        line = project.unicode2string_list(line)
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
    newline = project.unicode2_list(newline)
    if isinstance(newline,float):
        newline = int(newline)
        self.scenario_content.currentItem().setText(str(newline))
    # check if newline is int (wait) or not
    if type(newline) == int:
        pass
    # if we have a list as arguments, we need to keep a list
    elif len(newline) > 1:
        newline = [newline[0],newline[1:]]
    return newline