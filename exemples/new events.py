#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture

debug = True
lekture.debug = True

my_project = lekture.Project()

my_scenario = my_project.new_scenario()
other_scenario = my_project.new_scenario()
another_scenario = my_project.new_scenario()


print my_project.scenario()

del my_scenario

print my_project.scenario()
