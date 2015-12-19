

#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = False

my_project = lekture.Project('my_first_project',author='me and I',version='0.0.1')
my_scenario = lekture.Scenario(my_project,name='first',content=[['/pouett/no/yfughk',54678654]])
sleep(0.1)
my_poulscenario = lekture.Scenario(my_project,name='second')
sleep(0.1)
another_scenario = lekture.Scenario(my_project,name='third',content=[['zob',22]])
sleep(0.1)
another_scenario.content = [['/plouf' , 32]]


#for scenario in my_project.scenario():
#	print 'scenario :' , scenario.name


my_project.write()