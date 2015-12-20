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
print 'content' , my_scenario.content
for event in my_scenario.content:
	print 'event-name' ,event.name
	print 'event-name' ,event.content
print

another_scenario = my_project.new_scenario(content=['zob',22],name='lol')
another_scenario.content = [['/plouf' , 32]]

print 'la' , my_project.scenario()
my_project.del_scenario(my_scenario)
del my_scenario
print 'la' , my_project.scenario()
print

quit()

if my_project.scenario():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenario():
		print 'play scenario :' , scenario.name
		scenario.play()
