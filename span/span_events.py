import random
import span_functions as span
from OSC import OSCMessage
from devicemanager import OSCClient as OSCClient
client = OSCClient()
import time
from time import sleep

debug=True

db = {'data':{}}
objects = {}

def new(name='',protocol='',uid='',description = '',output='',event_content=''):
    """create an event"""
    if event_content == '':
        event_content={"0":{'/node/string':'a string','/node/integer':[random.randint(65e2,65e3)],'/node/float':[float(random.randint(0,100))/100],'/node/list':[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]}}
    if protocol == '':
        protocol = 'OSC'
    if output == '':
        output = '127.0.0.1:10000'
    if uid == '':
        uid = span.timestamp()
    if description == '':
        description = "write a comment"
    if name == '':
        name = 'untitled'
    if debug : print ("new event : " + uid)
    event_new = Event(uid=uid,name=name,output=output,description=description,event_content=event_content)
    objects.setdefault(uid,event_new)
    return uid

def play(name=''):
    uids=[]
    for event in listing():
        if name == event:
            uids.append(objects[event])
        elif db['data'][event]['attributes']['name'] == name:
            uids.append(objects[event])
    if len(uids) == 0:
        print "no event to play"
    for item in uids:
        item.play()

def listing():
    """make list of events (need to be done generic (make indexes from criteria)"""
    listing = db['data'].keys()
    return listing


class Event:
    """Create a new event"""
    def __init__(self,name,uid,description,event_content,output):
        db['data'].setdefault(uid, {'attributes' : {'name' : name , 'description' : description , 'content' : event_content , 'output' : output}})
        self.name=name
        self.output=output
        self.description=description
        self.content=event_content
        self.uid=uid
        if debug : 
            print
            print '---------INIT EVENT' , self.name , '-------------'
            print 'content : ' , self.content
            print 'name : ' , self.name
            print 'description : ' , self.description
            print 'output : ' , self.output
            print 'uid : ' , self.uid
            print

    def delete(self):
        """delete an event"""
        del db['data'][self.uid]

    def edit(self,attr,value):
        """edit an event attribute (name,output,description,content)"""
        if debug : print (self.uid + " EDIT : " + attr + ' -> ' , value)
        del db['data'][self.uid]['attributes'][attr]
        db['data'][self.uid]['attributes'].setdefault(attr,value)

    def timepoint_new(self):
        index = self.timepoint_available()
        db['data'][self.uid]['attributes']['content'].setdefault(index,{})
        print 'NEW TIMEPOINT' , index
        return index

    def timepoint_available(self,index = '0'):
        """create a timepoint in the selected event"""
        timepoints = db['data'][self.uid]['attributes']['content'].keys()
        #timepoints = sorted(timepoints)
        if str(index) not in timepoints:
            index = str(index)
            return index
        else:
            index = int(index) + 1
            return self.timepoint_available(index=index)

    def timepoint_delete(self,timepoint):
        """delete a timepoint in the selected event"""
        del db['data'][self.uid]['attributes']['content'][timepoint]

    def timepoints_listing(self):
        """list all timepoints"""
        return db['data'][self.uid]['attributes']['content'].keys()

    def play(self):
        """play an event"""
        if debug :
            print
            print '--------play event uid : ' + self.uid , '--------------'
        #output_ip = output.split(':')[0]
        #output_port = output.split(':')[1]
        #client.connect((output_ip , int(output_port)))
        client.connect(('127.0.0.1' , 1234))
        for timepoint in self.content.keys():
            sleep(float(timepoint)/1000)
            try:
                for address,args in self.content[timepoint].items():
                    msg = OSCMessage()
                    msg.setAddress(address)
                    msg.append(args)
                    client.send(msg)
                    time.sleep(0.01)
                    msg.clearData()
                if debug : print "timepoint sent" , timepoint
            except:
                print 'Connection refused'
        print '--------end event uid : ' + self.uid , '--------------'
        print
        return 'done'