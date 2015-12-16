#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep

from lekture import lekture

debug = True
lekture.debug = True

my_project = lekture.Project()

my_event = my_project.new_event()
other_event = my_project.new_event()
another_event = my_project.new_event()


print my_project.events()

del my_event

print my_project.events()
