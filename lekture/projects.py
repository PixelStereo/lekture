#!/usr/bin/env python
import os
import sys
import json
import random
from time import sleep
import random
import devicemanager
from OSC import OSCMessage , OSCClientError
from devicemanager import OSCClient as OSCClient
client = OSCClient()
import lekture

debug=True


# this is not the best way to do.
#But if i don't do that, I can't create scenario objects 
# because when I call Scenario.getinstances(), the instances list is empty
scenario_list = []
event_list = []
output_list = []

debug = True

class Project(object):
    """docstring for Project"""
    def __init__(self):
        super(Project, self).__init__()
        if debug == 2:
            print
            print "........... PROJECT created ..........."
            print 
        self.author = None
        self.version = None
        self.path = None
        self.lastopened = lekture.timestamp()
        self.new_output(self)

    def read(self,path) : 
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print "ERROR - THIS PATH IS NOT VALID" , path
        else :
            print 'loading' , path
            try:
                with open(path) as in_file :
                    """ TODO :  FIRST WE NEED TO CLEAR THE SCENARIO,DEVICES AND MODULAR APPLICATION INSTANCES"""
                    if debug : print 'file reading : ' , path
                    loaded = json.load(in_file,object_hook=lekture.unicode2string_dict)
                    in_file.close()
                    for key,val in loaded.items():
                        if key == 'scenario' :
                            for uid , scenario_dict in loaded['scenario'].items():
                                for attribute , value in scenario_dict['attributes'].items():
                                    if attribute == 'content':
                                        content = value
                                    elif attribute == 'name':
                                        name = value
                                    elif attribute == 'description':
                                        description = value
                                    elif attribute == 'output':
                                        output = value
                                self.new_scenario(self,uid=uid,name=name,description=description,output=output,content=content)
                        elif key == 'attributes' :
                            for attribute,value in loaded['attributes'].items():
                                if attribute == 'author':
                                    self.author = value
                                if attribute == 'version':
                                    self.version = value
                            self.lastopened = lekture.timestamp()
                        elif key == 'outputs' :
                            for index , out_dict in loaded['outputs'].items():
                                for attribute , value in out_dict['attributes'].items():
                                    if attribute == 'name':
                                        name = value
                                    if attribute == 'ip':
                                        adress_ip = value
                                    if attribute == 'udp':
                                        udp = value
                                self.new_output(self,index=index,name=name,ip=adress_ip,udp=udp)
                    if debug : print 'project loaded'
                    self.path = path
            except IOError:
                if debug : print 'error : project not loaded'
                return False
            return True

    def write(self,path=None) :
        if path:
            savepath = path
        else:
            savepath = self.path
        if savepath:
            if not savepath.endswith('.json'):
                savepath = savepath + '.json'
            out_file = open(str(savepath), 'w')
            project = {}
            project.setdefault('scenario',self.export_scenario())
            project.setdefault('attributes',self.export_attributes())
            project.setdefault('outputs',self.export_outputs())
            out_file.write(json.dumps(project,sort_keys = True, indent = 4,ensure_ascii=False).encode('utf8'))
            if debug : print ("file has been written : " , savepath)
            return True
        else:
            return False

    def scenarios(self):
        return Scenario.getinstances(self)

    def outputs(self):
        return Output.getinstances(self)

    def new_scenario(self,*args,**kwargs):
        taille = len(scenario_list)
        the_scenario = None
        scenario_list.append(the_scenario)
        scenario_list[taille] = Scenario(self)
        for key, value in kwargs.iteritems():
            setattr(scenario_list[taille], key, value)
        return scenario_list[taille]

    def new_output(self,*args,**kwargs):
        taille = len(output_list)
        the_output = None
        output_list.append(the_output)
        output_list[taille] = Output(self)
        for key, value in kwargs.items():
            setattr(output_list[taille], key, value)
        return output_list[taille]

    """def play_scenario(self,scenario):
        scenario.play()

    def scenario_obj(self):
        return scenario_list"""

    def del_scenario(self,scenario):
        scenario_list.remove(scenario)

    def export_attributes(self):
        attributes = {'author':self.author,'version':self.version,'lastopened':self.lastopened}
        return attributes

    def export_events(self):
        events = []
        for event in self.events():
            events.append({'attributes':{'output':event.output,'name':event.name,'description':event.description,'content':event.content}})
        return events
    
    def export_scenario(self):
        scenarios = []
        for scenario in self.scenarios():
            scenarios.append({'attributes':{'output':scenario.output,'name':scenario.name,'description':scenario.description,'events':scenario.export_events()}})
        return scenarios

    def export_outputs(self):
        outputs = []
        for output in self.outputs():
            outputs.append({'attributes':{'ip':output.ip,'udp':output.udp,'name':output.name}})
        return outputs


class Scenario(Project):
    """Create a new scenario"""
    def __init__(self,project,name='',uid='',description = '',output=''):
        """create an scenario"""
        if debug == 2:
            print
            print "........... SCENARIO created ..........."
            print
        if output == '':
            output = 1
        if uid == '':
            uid = lekture.timestamp()
        if description == '':
            description = "write a comment"
        if name == '':
            name = 'untitled'
        self.name=name
        self.project = project
        self.output=output
        self.description=description
        self.uid=uid
        self.new_event(content=['/node/integer',random.randint(65e2,65e3)]),self.new_event(content=random.randint(500,3000)),self.new_event(content=['/node/list',[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]])

    @staticmethod
    def getinstances(project):
        instances = []
        for scenario in scenario_list:
            if project == scenario.project:
                instances.append(scenario)
        return instances

    def events(self):
        return Event.getinstances(self)

    def new_event(self,*args,**kwargs):
        taille = len(event_list)
        the_event = None
        event_list.append(the_event)
        event_list[taille] = Event(self)
        for key, value in kwargs.iteritems():
            setattr(event_list[taille], key, value)
        return event_list[taille]

    def del_event(self,index):
        if type(index) == int:
            event_list.pop(index)
        else:
            event_list.remove(index)

    def play_from_here(self,index):
        index = event_list.index(index)
        self.play(index)

    def play(self,index=0):
        """play an scenario
        Started from the first event if an index has not been provided"""
        if debug : print '------ PLAY SCENARIO :' , self.name , 'FROM INDEX' , index , '-----'
        for event in self.events()[index:]:
            event.play()
        return self.name , 'play done'


class Event(object):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, scenario,content=[],name='',description='',output=''):
        if debug == 2:
            print
            print "........... Event created ..........."
            print
        if output == '':
            output = 1
        if description == '':
            description = "event's description"
        if name == '':
            name = 'untitled event'
        if content == []:
            content = ['no content for this event']
        self.name=name
        self.scenario = scenario
        self.output=output
        self.description=description
        self.content = content
        
    @staticmethod
    def getinstances(scenario):
        instances = []
        for event in event_list:
            if scenario == event.scenario:
                instances.append(event)
        return instances

    def play(self):
        if type(self.content) is int or type(self.content) is float:
            wait = float(self.content)
            wait = wait/1000
            if debug : print 'waiting' , wait
            sleep(wait)
        else:
            address = self.content[0]
            args = self.content[1:]
            output_ip = self.getoutput(self.output).ip
            output_port = self.getoutput(self.output).udp
            for arg in args:
                try:
                    if debug : 
                        print 'connecting to : ' + output_ip + ':' + str(output_port)
                    client.connect((output_ip , int(output_port)))
                    msg = OSCMessage()
                    msg.setAddress(address)
                    msg.append(arg)
                    client.send(msg)
                    sleep(0.001)
                    msg.clearData()
                except OSCClientError :
                    print 'Connection refused'

    def getoutput(self,index):
        if index > 0 and index <= len(Output.getinstances(self.scenario.project)):
            index = index - 1
            return Output.getinstances(self.scenario.project)[index]
        else:
            return False


class Output(Project):
    """Create a new output"""
    def __init__(self,project,ip='127.0.0.1',name='no-name',udp =10000,index=None):
        if debug == 2:
            print
            print "........... OUTPUT created ..........."
            print
        index = len(output_list)
        self.name=name
        self.udp = udp
        self.ip=ip
        self.index=index
        self.project = project

    @staticmethod
    def getinstances(project):
        instances = []
        for output in output_list:
            if project == output.project:
                instances.append(output)
        return instances
