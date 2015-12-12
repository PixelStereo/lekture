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
print my_event.protocol
print my_event.description
print my_event.output
print my_event.content
print my_event.content.keys()
print"""
my_event.timepoint(10)

another_event = lekture.events.Event(content={'zob':22},name='lol')
print '------'
another_event.content = {'plouf' : 32}

""" content doesn't work when creating a timepoint… AHHHHHHHH"""
another_event.timepoint(1000,content={'/my_string':['blah',2]})

print another_event.content

print
print 'events listing'
print '--------------'
for event in lekture.events.Event.instances.keys():
    print 'event named' , event.name , ':' , event
    for timepoint in event.timepoints:
        print '     ' ,  'timepoint' , timepoint.index , ':' , timepoint.content
