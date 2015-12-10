from span import span
from time import sleep

span.debug = False
span.events.debug = True

span.read(path='span/projects/test.json')


span.events.play('et de quatre')
sleep(1)
span.events.play('second')
sleep(1)
span.events.play('troisieme')
sleep(1)
span.events.play('first')
quit()

quit()

try :
    while 1 :
        pass
except KeyboardInterrupt :
    print "\nClosing OSCClient and OSCServer"
    osc.close()
    st.join()
    print "Done"