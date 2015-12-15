from lekture import lekture
from time import sleep

# create a project
my_project = lekture.Project()

my_project.read()

print 'name' , my_project.name

for event in my_project.events():
	event.play()

my_project.write()