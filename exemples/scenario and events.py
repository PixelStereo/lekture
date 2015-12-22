#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/pyprojekt')
sys.path.append(lib_path)
import projekt

debug = True
projekt.debug = True

my_project = projekt.new_project()
my_project.name = 'pouette'

my_other_project = projekt.new_project()
my_other_project.name = 'other'
my_other_project.author = 'me and I'
my_other_project.version = '2.2.1'

my_scenario = my_project.new_scenario()
my_project.name = 'toto-la-roulette'
print 'name' , my_scenario.name
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

for project in projekt.projects():
	print 'path' ,  project.path
	print 'version' ,  project.version
	print 'author' , project.author
	for scenario in project.scenarios():
		print 'scenario :' , scenario.name
	print

if projekt.projects():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenarios():
		print 'play scenario :' , scenario.name
		scenario.play()
		
if my_project.scenarios():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenarios():
		print 'play scenario :' , scenario.name
		scenario.play()

print 'how many scenario :' , len(my_project.scenarios()) , my_project.scenarios()
#my_project.del_scenario(my_scenario)
print 'how many scenario :' , len(my_project.scenarios()) , my_project.scenarios()

my_project.path = 'test_project.json'
my_project.write()


