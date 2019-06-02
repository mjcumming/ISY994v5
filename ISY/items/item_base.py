#! /usr/bin/env python

''' 

Base Device

Common to all ISY items ie programs, variables, devices, scenes

status property -> ready, alert, lost


'''



class Item_Base(object):

    def __init__(self, container, name):
        self.container = container

        self.name = name

        self.properties = {'status' : 'init'} # list of properties key = property name, value = property value

        self.property_event_handlers = []

    def process_websocket_event(self,event):
        pass # classes to override

    def add_property(self, property_, value = None):
        self.properties [property_] = value

    def set_property(self, property_, value, always_publish=False): # propagates up to the container and to handlers
        if self.properties [property_] != value or always_publish:
            self.properties [property_] = value
            self.container.property_change(self,property_,value) 

            for handler in self.property_event_handlers:
                handler (property_,value)
 
    def get_property(self, property_):
        return self.properties [property_] 

    def send_request(self,path,query=None,timeout=None): 
        return self.container.send_request(path,query,timeout)

    def add_property_event_handler(self,handler):
        self.property_event_handlers.append(handler)

    def get_identifier(self):
        pass # subclasses to provide