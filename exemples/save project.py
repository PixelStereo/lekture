import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
print 'yy' ,  lib_path
sys.path.append(lib_path)
import lekture
from time import sleep

my_projekt = lekture.Project('test-projekt')

#create an event
event = my_projekt.new_event(name='event')

#need to be sure that it doesn't have the same uid (included it in events.new????)
sleep(0.01)

#create another event
another_event = my_projekt.new_event(name="another event")

print 'list events'
print '------------'
for event in my_projekt.events():
	print event.name

#play cues
event.play()
sleep(1)
another_event.play()


# save the projekt 
my_projekt.path = os.path.abspath('lekture/projects/'+lekture.timestamp()+'.json')
my_projekt.write()