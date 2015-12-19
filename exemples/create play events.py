#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = True

my_project = lekture.new_project(name='pouette')

my_scenario = my_project.new_scenario(name='toto-la-roulette')
"""print my_scenario.name
print my_scenario.uid
print my_scenario.description
print my_scenario.output
print my_scenario.contentç
print my_scenario.content.keys()
print"""

another_scenario = my_project.new_scenario(content=[['zob',22]],name='lol')
another_scenario.content = [['/plouf' , 32]]

print my_project.scenario()

del my_scenario

print my_project.scenario()

print
print
if my_project.scenario():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenario():
		print 'play scenario :' , scenario.name
		scenario.play()