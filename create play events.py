#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep

from lekture import lekture

debug = True
lekture.debug = True
lekture.events.debug = True

my_event = lekture.events.Event(name='toto-la-roulette')
"""print my_event.name
print my_event.uid
print my_event.description
print my_event.output
print my_event.contentç
print my_event.content.keys()
print"""

another_event = lekture.events.Event(content=[['zob',22]],name='lol')
another_event.content = [['/plouf' , 32]]

print lekture.events.Event.instances.keys()

del my_event

print lekture.events.Event.instances.keys()

print
print
if lekture.events.Event.instances.keys():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for event in lekture.events.Event.instances.keys():
		print 'play event :' , event.name
		event.play()