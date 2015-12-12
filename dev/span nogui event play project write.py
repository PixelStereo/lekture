import os, sys
lib_path = os.path.abspath('./../')
print lib_path
sys.path.append(lib_path)

from lekture import lekture
from time import sleep


#create an event
lekture.events.new(name='event')

#need to be sure that it doesn't have the same uid (included it in events.new????)
sleep(0.01)

#create another event
lekture.events.new(name="another event")

#list existing events
print lekture.events.listing()

#play the cue
lekture.events.play(name='event')

sleep(1)

#play the cue
lekture.events.play(name="another event")

#save the project
lekture.write()

sleep(5)
quit()
