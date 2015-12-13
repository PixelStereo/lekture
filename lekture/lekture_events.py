import weakref
import random
import lekture_functions as lekture
from OSC import OSCMessage , OSCClientError
from devicemanager import OSCClient as OSCClient
client = OSCClient()
import time
from time import sleep

debug=True


class Timepoint(object):
    """docstring for Timepoint"""
    def __new__(self,*args,**kwargs):
        _new = object.__new__(self)
        if debug :
            print "........... TIMEPOINT created ..........."
        return _new

    def __init__(self,index,content={}):
        if content == {}:
            content = {'/node/string':'a string','/node/integer':[random.randint(65e2,65e3)],'/node/float':[float(random.randint(0,100))/100],'/node/list':[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]}
        self.index = index
        self.content = content
        if debug : 
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

    def timepoint(self,index,content={}):
        """create a timepoint"""
        timepoint = Timepoint(index,content={})
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

    def play(self):
        """play an event"""
        if debug : print '------ PLAY EVENT :' , self.name , '-----------------'
        timepoints = []
        for timepoint in self.timepoints:
            timepoints.append([timepoint.index,timepoint])
        timepoints.sort()
        for timepoint in timepoints:
            if debug : print '--------PLAY TIMEPOINT' , timepoint[0] , '----------'
            sleep(timepoint[0]/1000)
            output_ip = self.output.split(':')[0]
            output_port = self.output.split(':')[1]
            if debug : 
                print 'connecting to : ' + output_ip + ':' + output_port
                if debug : 'try to send timepoint ' , timepoint.index
            try:
                client.connect((output_ip , int(output_port)))
                for address,args in timepoint[1].content.items():
                    if debug : print address , args
                    msg = OSCMessage()
                    msg.setAddress(address)
                    msg.append(args)
                    client.send(msg)
                    time.sleep(0.01)
                    msg.clearData()
                if debug :
                    print '--------END timepoint' , timepoint[0] , '--------------'
                    print
            except OSCClientError :
                print 'Connection refused'
        return self.name , 'done'




    def delete(self):
        """delete an event"""
        del db['data'][self.uid]

    def edit(self,attr,value):
        """edit an event attribute (name,output,description,content)"""
        if debug : print (self.uid + " EDIT : " + attr + ' -> ' , value)
        del db['data'][self.uid]['attributes'][attr]
        db['data'][self.uid]['attributes'].setdefault(attr,value)



