#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = True

my_project = lekture.new_project()
my_project.name = 'pouette'

my_scenario = my_project.new_scenario()
my_project.name = 'toto-la-roulette'
print 'name' , my_scenario.name
print 'uid' , my_scenario.uid
print 'description' , my_scenario.description
print 'output' , my_scenario.output
for event in my_scenario.events():
	print 'event-name' ,event.name
	print 'event-name' ,event.content
print

another_scenario = my_project.new_scenario()
print 'content before' , len(another_scenario.events())
an_event = another_scenario.new_event(content=1000)
an_event = another_scenario.new_event(content=['/zob',232])
print 'content after' , len(another_scenario.events())

an_event.play()
an_event.content = ['/plouf' , 32]
print an_event.content
an_event.play()
another_scenario.play()


if my_project.scenario():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenario():
		print 'play scenario :' , scenario.name
		scenario.play()

print 'how many scenario :' , len(my_project.scenario()) , my_project.scenario()
#my_project.del_scenario(my_scenario)
print 'how many scenario :' , len(my_project.scenario()) , my_project.scenario()

my_project.path = '/Users/reno/Desktop/toto.json'
my_project.write()


