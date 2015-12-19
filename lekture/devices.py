from OSC import OSCMessage
from devicemanager import OSCClient as OSCClient
import time
from time import sleep

debug=True

db = {}
objects = {}

def new_OSC(uid='',port='',ip=''):
    """create an OSC Device"""
    if port == '':
        port = '1234'
    if ip == '':
        ip = '127.0.0.1'
    if name == '':
        name = 'osc_device'
    if debug : print ("new osc device : " + name + ' registered at ' + ip+':'+port)
    osc_new = OSC(name=name,port=port,ip=ip)
    objects.setdefault(name,osc_new)
    return name

def listing():
    """make list of devices (need to be done generic (make indexes from criteria)"""
    listing = db.keys()
    return listing


class OSC:
    """Create an OSC device"""
    def __init__(self,name,port='1234',ip='127.0.0.1'):
        db.setdefault(name, {'port':port,'ip':ip})
        self.name=name
        self.ip=ip
        self.port=port
        if debug : print 'name : ' , self.name
        if debug : print 'port : ' , self.port
        if debug : print 'ip : ' , self.ip
        self.client = OSCClient()

    def delete(self):
        """delete an scenario"""
        del db[self.name]

    def edit(self,attr,value):
        """edit a device attribute (ip,port)"""
        if debug : print (self.name + " EDIT : " + attr + ' -> ' , value)
        del db[self.name]['attributes'][attr]
        db[self.name]['attributes'].setdefault(attr,value)

