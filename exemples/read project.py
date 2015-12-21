#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
lib_path = os.path.abspath('./../../lekture/pyprojekt')
sys.path.append(lib_path)
import projekt
from time import sleep

# create a project
my_project = projekt.new_project()

my_project.read(path='test.json')
print '-----------------------------------------'

for scenario in my_project.scenarios():
	print 'name :' , scenario.name
	for event in scenario.events():
		print 'event :' , event.content

for scenario in my_project.scenarios():
	scenario.play()

my_project.write()