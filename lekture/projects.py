#!/usr/bin/env python
import os
import sys
import json
import random
import weakref
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
output_list = []

debug = True

class Project(object):
    """docstring for Project"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self):
        _new = object.__new__(self)
        Project.instances[_new] = None
        if debug :
            print
            print "........... PROJECT created ..........."
            print 
        return _new

    def __init__(self):
        super(Project, self).__init__()
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

    def scenario(self):
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

    def play_scenario(self,scenario):
        scenario.play()

    def scenario_obj(self):
        return scenario_list

    def del_scenario(self,scenario):
        scenario_list.remove(scenario)

    def del_scenario_line(self,scenario,index):
        scenario.content.pop(index)

    def export_attributes(self):
        attributes = {'author':self.author,'version':self.version,'lastopened':self.lastopened}
        return attributes

    def getoutput(self,index):
        if index > 0 and index <= len(Output.getinstances(self)):
            index = index - 1
            return Output.getinstances(self)[index]
        else:
            return False

    def export_scenario(self):
        scenario = {}
        for scenario in self.scenario():
            scenario.setdefault(scenario.uid,{'attributes':{'content':scenario.content,'output':scenario.output,'name':scenario.name,'description':scenario.description}})
        return scenario

    def export_outputs(self):
        outputs = {}
        for output in self.outputs():
            outputs.setdefault(output.index,{'attributes':{'ip':output.ip,'udp':output.udp,'name':output.name}})
        return outputs


class Scenario(Project):
    """Create a new scenario"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self,project,*args,**kwargs):
        _new = object.__new__(self,project)
        Scenario.instances[_new] = None
        if debug :
            print
            print "........... SCENARIO created ..........."
            print
        return _new

    def __init__(self,project,name='',uid='',description = '',output='',content=[]):
        """create an scenario"""
        if output == '':
            output = 1
        if uid == '':
            uid = lekture.timestamp()
        if description == '':
            description = "write a comment"
        if name == '':
            name = 'untitled'
        if content == []:
            content = [['/node/string','a string'],random.randint(500,3000),['/node/integer',random.randint(65e2,65e3)],['/node/float',float(random.randint(0,100))/100],['/node/list',[float(random.randint(0,100))/100,random.randint(65e2, 65e3),"egg"]]]            
        self.name=name
        self.project = project
        self.output=output
        self.description=description
        self.uid=uid
        self.content = content

    @staticmethod
    def getinstances(project):
        instances = []
        for scenario in Scenario.instances.keys():
            if project == scenario.project:
                instances.append(scenario)
        return instances

    # ----------- CONTENT -------------
    @property
    def content(self):
        "Current content of the scenario"
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @content.deleter
    def content(self):
        pass


    # ----------- NAME -------------
    @property
    def name(self):
        "Current name of the scenario"
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        pass

    # ----------- UID -------------
    @property
    def uid(self):
        "Current uid of the scenario"
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
        "Current description of the scenario"
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
        "Current output of the scenario"
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output

    @output.deleter
    def output(self):
        pass

    def play(self):
        """play an scenario"""
        if debug : print '------ PLAY SCENARIO :' , self.name , '-----------------'
        for line in self.content:
            if type(line) is int or type(line) is float:
                line = int(line)
                if debug : print 'waiting' , line
                sleep(line/1000)
            else:
                output_ip = self.project.getoutput(1).ip
                output_port = self.project.getoutput(1).udp
                #output_ip = self.output.split(':')[0]
                #output_port = self.output.split(':')[1]
                if debug : 
                    print 'todo : use bundle for each packet between wait'
                    print 'connecting to : ' + output_ip + ':' + str(output_port)
                try:
                    client.connect((output_ip , int(output_port)))
                    msg = OSCMessage()
                    msg.setAddress(line[0])
                    msg.append(line[1:])
                    client.send(msg)
                    sleep(0.01)
                    msg.clearData()
                except OSCClientError :
                    print 'Connection refused'
        return self.name , 'done'



class Output(Project):
    """Create a new scenario"""
    instances = weakref.WeakKeyDictionary()
    def __new__(self,project,*args,**kwargs):
        _new = object.__new__(self,project)
        Output.instances[_new] = None
        if debug :
            print
            print "........... OUTPUT created ..........."
            print
        return _new

    def __init__(self,project,ip='127.0.0.1',name='no-name',udp =10000,index=None):
        """create an output"""
        index = len(self.instances)
        self.name=name
        self.udp = udp
        self.ip=ip
        self.index=index
        self.project = project

    @staticmethod
    def getinstances(project):
        instances = []
        for output in Output.instances.keys():
            if project == output.project:
                instances.append(output)
        return instances

    # ----------- IP -------------
    @property
    def ip(self):
        "Current ip of the output"
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @ip.deleter
    def ip(self):
        pass


    # ----------- NAME -------------
    @property
    def name(self):
        "Current name of the output"
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        pass

    # ----------- UDP -------------
    @property
    def udp(self):
        "Current udp of the output"
        return self.__udp

    @udp.setter
    def udp(self, udp):
        self.__udp = udp

    @udp.deleter
    def udp(self):
        pass
