#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

debug=1

def unicode2string_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = unicode2string_list(value)
        elif isinstance(value, dict):
            value = unicode2string_dict(value)
        rv[key] = value
    return rv

def unicode2string_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = unicode2string_list(item)
        elif isinstance(item, dict):
            item = unicode2string_dict(item)
        rv.append(item)
    return rv

def read() : 
    path = os.path.abspath('/Users/reno/Desktop/one event.scorejson')
    if not os.path.exists(path):
        print "ERROR - THIS PATH IS NOT VALID" , path
    else :
        print 'loading' , path
        try:
            with open(path) as in_file :
                """ TODO :  FIRST WE NEED TO CLEAR THE EVENTS,DEVICES AND MODULAR APPLICATION INSTANCES"""
                if debug : print 'file reading : ' , path
                loaded = json.load(in_file,object_hook=unicode2string_dict)
                in_file.close()
                for key,val in loaded.items():
                    if key == 'Document' :
                        for key , value in loaded['Document'].items():
                            if key == 'BaseScenario':
                                print 'BaseScenario is :'
                                print value.keys()
                                print
                            if key == 'ObjectName':
                                print 'ObjectName is :' , value
                            if key == 'DocumentId':
                                print 'DocumentId is :' , value
                            if key == 'id':
                                print 'id is :' , value
                for key , value in loaded['Plugins'].items():
                    print key
                    if key == 'DeviceDocumentPlugin':
                        print 'DeviceDocumentPlugin is :' , value
                    if key == 'OSSIADocumentPlugin':
                        print 'OSSIADocumentPlugin is :' , value
                if debug : print 'project loaded'
        except IOError:
            if debug : print 'error : project not loaded'
            return False
        return True

read()