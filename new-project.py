

#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep

from lekture import lekture

debug = True
lekture.debug = False

my_project = lekture.new_project()

quit()


my_other_project = lekture.Project('other',author='me and I',version='2.2.1')

my_event = lekture.Event(my_project,name='toto-la-roulette')
my_poulevent = lekture.Event(my_project,name='qlsi qsdipu qd')

another_event = lekture.Event(my_project,name='lol',content=[['zob',22]])
another_event.content = [['/plouf' , 32]]


for project in lekture.Project.instances.keys():
	print 'project' , project.name
	print 'path' ,  project.path
	print 'name' , project.name
	print 'version' ,  project.version
	print 'author' , project.author
	for event in project.events():
		print 'event :' , event.name
	print

if lekture.Event.instances.keys():
	print 'PLAY ALL EVENTS'
	print '--------------'
	for event in my_project.events():
		print 'play event :' , event.name
		event.play()

#my_project.write()