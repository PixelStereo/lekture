import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture
from time import sleep

# create a project
my_project = lekture.new_project()

my_project.read(path='lekture/projects/test.json')

print 'name' , my_project.name
print '-----------------------------------------'
print '-----------------------------------------'
for scenario in my_project.scenario():
	print 'name :' , scenario.name
	print 'content :' , scenario.content

for scenario in my_project.scenario():
	scenario.play()

my_project.write()