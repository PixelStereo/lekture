import weakref
import random
import lekture_functions as lekture
from OSC import OSCMessage
from devicemanager import OSCClient as OSCClient
client = OSCClient()
import time
from time import sleep

debug=True


""" TODO : REWRITE PLAY - DELETE FUNCTIONS FOR TIMEPOINT AND EVENT CLASS"""

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


class Timepoint(object):
    """docstring for Timepoint"""
    def __new__(self,index,content={}):
        _new = object.__new__(self)
        if debug :
            print
            print "........... TIMEPOINT created ..........."
        return _new

    def __init__(self,index,content={}):
        if content == {}:
            content = {'/node/string':'a string','/node/integer':[random.randint(65e2,65e3)],'/node/float':[float(random.randint(0,100))/100],'/node/list':[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]}
        self.index = index
        self.content = content
        print 'TIMEPOINT INDEX' , self.index
        print 'TIMEPOINT CONTENT' , self.content
        print "........... TIMEPOINT %s inited ..........." %str(index)
        print

    # ----------- CONTENT -------------
    @property
    def content(self):
        "Current content of the timepoint"
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @content.deleter
    def content(self):
        pass


class Event(object):
    """Create a new event"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self,*args,**kwargs):
        _new = object.__new__(self)
        Event.instances[_new] = None
        if debug :
            print
            print "........... EVENT created ..........."
            print
        return _new

    def __init__(self,name='',protocol='',uid='',description = '',output='',content=''):
        """create an event"""
        timepoints = []
        if protocol == '':
            protocol = 'OSC'
        if output == '':
            output = '127.0.0.1:10000'
        if uid == '':
            uid = lekture.timestamp()
        if description == '':
            description = "write a comment"
        if name == '':
            name = 'untitled'
        self.name=name
        self.output=output
        self.description=description
        self.protocol = protocol
        self.uid=uid
        self.timepoints = timepoints
        self.timepoint(0)
        if content != '' : 
            self.content=content
        if debug : 
            print
            print "........... EVENT %s initing ..........." %self.name
            for timepoint in self.timepoints:
                print 'timepoint' , timepoint.index , ':' , timepoint.content
            print 'name : ' , self.name
            print 'description : ' , self.description
            print 'output : ' , self.output
            print 'uid : ' , self.uid
            print "........... EVENT %s inited ..........." %self.name
            print


    def timepoint(self,index):
        """create a timepoint"""
        timepoint = Timepoint(index)
        self.timepoints.append(timepoint)
        return timepoint


    # ----------- CONTENT -------------
    @property
    def content(self):
        "Current content of the event (shortcut to timepoint 0) - TODO : CONCATENATE ALL TIMEPOINTS"
        return self.timepoints[0].content

    @content.setter
    def content(self, content):
        self.timepoints[0].content = content

    @content.deleter
    def content(self):
        pass

    # ----------- TIMEPOINTS -------------
    @property
    def timepoints(self):
        "Current timepoints of the event"
        return self.__timepoints

    @timepoints.setter
    def timepoints(self, timepoints):
        self.__timepoints = timepoints

    @timepoints.deleter
    def timepoints(self):
        pass

    # ----------- NAME -------------
    @property
    def name(self):
        "Current name of the event"
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        pass

    # ----------- PROTOCOL -------------
    @property
    def protocol(self):
        "Current protocol of the event"
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):
        self.__protocol = protocol

    @protocol.deleter
    def protocol(self):
        pass

    # ----------- UID -------------
    @property
    def uid(self):
        "Current uid of the event"
        return self.__uid

    @uid.setter
    def uid(self, uid):
        self.__uid = uid

    @uid.deleter
    def uid(self):
        pass

    # ----------- DECRIPTION -------------
    @property
    def description(self):
        "Current description of the event"
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @description.deleter
    def description(self):
        pass

    # ----------- OUTPUT -------------
    @property
    def output(self):
        "Current output of the event"
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output

    @output.deleter
    def output(self):
        pass





    def delete(self):
        """delete an event"""
        del db['data'][self.uid]

    def edit(self,attr,value):
        """edit an event attribute (name,output,description,content)"""
        if debug : print (self.uid + " EDIT : " + attr + ' -> ' , value)
        del db['data'][self.uid]['attributes'][attr]
        db['data'][self.uid]['attributes'].setdefault(attr,value)

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

