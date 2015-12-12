from lekture import lekture
from time import sleep

lekture.debug = False
lekture.events.debug = True

lekture.read(path='lekture/projects/test.json')


lekture.events.play('et de quatre')
sleep(1)
lekture.events.play('second')
sleep(1)
lekture.events.play('troisieme')
sleep(1)
lekture.events.play('first')
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