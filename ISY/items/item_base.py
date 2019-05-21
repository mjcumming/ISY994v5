#! /usr/bin/env python

''' 

Base Device

Common to all ISY items ie programs, variables, devices, scenes


status property -> ready, alert, lost

'''



class Item_Base(object):

    def __init__(self, container):
        self.container = container

        self.properties = {'status' : None} # list of properties key = property name, value = property value

    def process_websocket_event(self,event):
        pass # classes to override

    def add_property(self, property_, value = None):
        self.properties [property_] = value

    def set_property(self, property_, value): # propagates up to the container 
        self.properties [property_] = value
        self.container.property_change(self,property_,value) 
 
    def get_property(self, property_):
        return self.properties [property_] 

    def send_request(self,path,query=None,timeout=None): 
        return self.container.send_request(path,query,timeout)