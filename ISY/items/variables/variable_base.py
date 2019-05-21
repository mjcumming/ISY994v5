#! /usr/bin/env python

''' 

Base Variable

Common to all elements returned from rest/nodes/variables

   properties = list of properties and values

'''



class Variable_Base(object):

    def __init__(self, container, variable_info): 
        self.container = container

        self.properties = {'status' : 'ready'} # list of properties key = property name, value = property value
            
        self.id = variable_info.id
        self.type = variable_info.type
        self.name = self.id # replaced once names are retrieved

        self.add_property ('init_value', variable_info.init_value)
        self.add_property ('value', variable_info.value)
        self.add_property ('time_set', variable_info.time_set)

    def get_index(self): # creates an index using var type and id
        return self.type+':'+self.id

    def __str__(self):
        return ("Variable: {} ; index {} ; value {}".format(self.name, self.get_index(), self.get_property('value')))

    def process_websocket_event(self,event):
        var_node = event.event_info_node.find('var')
        value = var_node.find('val').text
        time_set = var_node.find('ts').text

        self.set_property ('value',value)
        self.set_property ('time_set',time_set)

    def add_property(self, property_,value = None):
        self.properties [property_] = value

    def set_property(self, property_, value):
        self.properties [property_] = value
        self.container.variable_property_change(self,property_,value) 
 
    def get_property(self, property_):
        return self.properties [property_]
 
    def send_request(self,path,query=None,timeout=None): 
        return self.container.send_request(path,query,timeout)

    def device_event(self,device): #device event, process and see if we are interested
        pass # subclasses to provide