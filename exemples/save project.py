

#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/pyprojekt')
sys.path.append(lib_path)
import projekt

debug = True
projekt.debug = False

my_project = projekt.new_project()
my_project.name = 'my_first_project'
my_project.author = 'me and I'
my_project.version = '0.0.1'

my_scenario = my_project.new_scenario()
my_scenario.name = 'first'
my_event = my_scenario.new_event()
my_event.content = [['/pouett/no/yfughk',54678654]]
sleep(0.1)
my_poulscenario = my_project.new_scenario()
my_poulscenario.name = 'second'
sleep(0.1)
another_scenario = my_project.new_scenario()
another_scenario.name = 'third'
another_scenario.content = [['zob',22]]
sleep(0.1)
another_scenario.content = [['/plouf' , 32]]

for scenario in my_project.scenarios():
	print 'scenario :' , scenario.name
	for event in scenario.events():
		print 'event :', event.content

my_project.path = 'test.json'
my_project.write()