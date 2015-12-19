

#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = False

my_project = lekture.Project('first',author='me and I',version='2.2.1')

my_other_project = lekture.Project('other',author='me and I',version='2.2.1')

my_scenario = lekture.Scenario(my_project,name='toto-la-roulette')
my_poulscenario = lekture.Scenario(my_project,name='qlsi qsdipu qd')

another_scenario = lekture.Scenario(my_project,name='lol',content=[['zob',22]])
another_scenario.content = [['/plouf' , 32]]


for project in lekture.Project.instances.keys():
	print 'project' , project.name
	print 'path' ,  project.path
	print 'name' , project.name
	print 'version' ,  project.version
	print 'author' , project.author
	for scenario in project.scenario():
		print 'scenario :' , scenario.name
	print

if lekture.Scenario.instances.keys():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for scenario in my_project.scenario():
		print 'play scenario :' , scenario.name
		scenario.play()

my_project.write()