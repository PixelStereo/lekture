import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
print 'yy' ,  lib_path
sys.path.append(lib_path)
import lekture
from time import sleep

# create a project
my_project = lekture.Project()

my_project.read(path='lekture/projects/test.json')

print 'name' , my_project.name
print '-----------------------------------------'
print '-----------------------------------------'
for event in my_project.events():
	print 'name :' , event.name
	print 'content :' , event.content

for event in my_project.events():
	event.play()

my_project.write()