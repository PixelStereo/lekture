import os, sys
lib_path = os.path.abspath('./../')
print lib_path
sys.path.append(lib_path)

from span import span
from time import sleep


#create an event
span.events.new(name='event')

#need to be sure that it doesn't have the same uid (included it in events.new????)
sleep(0.01)

#create another event
span.events.new(name="another event")

#list existing events
print span.events.listing()

#play the cue
span.events.play(name='event')

sleep(1)

#play the cue
span.events.play(name="another event")

#save the project
span.write()

sleep(5)
quit()
