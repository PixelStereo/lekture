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
print lekture.events.Event.instances.keys()

#list existing events
#print lekture.events.listing()
for event in lekture.events.Event.instances.keys():
	print event.name

#play the cue
lekture.events.play(name='event')

sleep(1)

#play the cue
lekture.events.play(name="another event")

#save the project
#lekture.write()

sleep(5)
quit()
