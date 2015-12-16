

#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
print 'yy' ,  lib_path
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = False

my_project = lekture.Project('my_first_project',author='me and I',version='0.0.1')
my_event = lekture.Event(my_project,name='first',content=[['/pouett/no/yfughk',54678654]])
sleep(0.1)
my_poulevent = lekture.Event(my_project,name='second')
sleep(0.1)
another_event = lekture.Event(my_project,name='third',content=[['zob',22]])
sleep(0.1)
another_event.content = [['/plouf' , 32]]


#for event in my_project.events():
#	print 'event :' , event.name


my_project.write()