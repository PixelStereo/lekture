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

my_event = my_project.new_event()
other_event = my_project.new_event()
another_event = my_project.new_event()


print my_project.events()

del my_event

print my_project.events()
