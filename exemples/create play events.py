#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
print 'yy' ,  lib_path
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = True

my_project = lekture.new_project(name='pouette')

my_event = my_project.new_event(name='toto-la-roulette')
"""print my_event.name
print my_event.uid
print my_event.description
print my_event.output
print my_event.contentç
print my_event.content.keys()
print"""

another_event = my_project.new_event(content=[['zob',22]],name='lol')
another_event.content = [['/plouf' , 32]]

print my_project.events()

del my_event

print my_project.events()

print
print
if my_project.events():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for event in my_project.events():
		print 'play event :' , event.name
		event.play()