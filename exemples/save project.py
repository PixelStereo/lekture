import os,sys
lib_path = os.path.abspath('./../../lekture/lekture')
sys.path.append(lib_path)
import lekture
from time import sleep

my_projekt = lekture.Project('test-projekt')

#create an scenario
scenario = my_projekt.new_scenario(name='scenario')

#need to be sure that it doesn't have the same uid (included it in scenario.new????)
sleep(0.01)

#create another scenario
another_scenario = my_projekt.new_scenario(name="another scenario")

print 'list scenario'
print '------------'
for scenario in my_projekt.scenario():
	print scenario.name

#play cues
scenario.play()
sleep(1)
another_scenario.play()


# save the projekt 
my_projekt.path = os.path.abspath('lekture/projects/'+lekture.timestamp()+'.json')
my_projekt.write()