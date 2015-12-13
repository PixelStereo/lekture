from lekture import lekture
from time import sleep


#create an event
event = lekture.events.Event(name='event')

#need to be sure that it doesn't have the same uid (included it in events.new????)
sleep(0.01)

#create another event
another_event = lekture.events.Event(name="another event")

print 'list events'
print '------------'
for event in lekture.events.Event.instances.keys():
	print event.name

#play cues
event.play()
sleep(1)
another_event.play()

#save the project
filepath = lekture.abspath(lekture.timestamp()+'.json')
lekture.write(filepath)