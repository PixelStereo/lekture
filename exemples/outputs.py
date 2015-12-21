#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/pyprojekt')
sys.path.append(lib_path)
import projekt

debug = True
projekt.debug = True
projekt.test = False

# create a project
my_project = projekt.new_project()
another_project = projekt.new_project()
"""When creating a project, an output is created, default is 127.0.0.1:10000"""

# create another output
second_out = my_project.new_output()
second_out.name = 'another output'
second_out.ip = socket.gethostbyname(socket.gethostname())
second_out.udp = 1234
print second_out

# iterate outputs
out_counter = 0
for output in my_project.outputs():
	out_counter += 1
	print 'output n°'+str(out_counter)+' :' , output.name , output.ip + ':' + str(output.udp)

# create a scenario
my_scenario = my_project.new_scenario()

# create an event
my_event = my_scenario.new_event(content=['/zob',232])

#play first scenario with default output
my_scenario.play()

#play first scenario with second output
my_scenario.output = 2
"""THE PRIBLEM CAN BE SEEN HERE. THE OUTPUT OF SCENARIO IS NOT IN THE SCENARIO LIST. WHO CREATES AN OUTPUT WHICH IS NOT IN THE INSTANCES LIST ????????"""
print my_project.outputs().index(my_scenario.getoutput())
print 'new output' , my_scenario.output , my_scenario.getoutput() , my_project.outputs()
my_scenario.play()

"""when creating a scenario, its default output is 1, the default output of the project
When creating an event, it doesn't have an output. It use output's scenario. But you can assing an output for an event if you want"""
my_event.output = 1
my_scenario.play()
