from lekture import lekture
from time import sleep

# create a project
my_project = lekture.Project()

my_project.read()

#for event in lekture.events.Event.getinstances():
#	event.play()

my_project.write()