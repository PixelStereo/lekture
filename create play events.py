#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep

from lekture import lekture

debug = True
lekture.debug = True

my_project = lekture.Project('pouette')

my_event = my_project.new_event(name='toto-la-roulette')
"""print my_event.name
print my_event.uid
print my_event.description
print my_event.output
print my_event.contentç
print my_event.content.keys()
print"""

another_event = lekture.Event(my_project ,content=[['zob',22]],name='lol')
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