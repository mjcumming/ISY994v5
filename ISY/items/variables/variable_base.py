#! /usr/bin/env python

''' 

Base Variable

Common to all elements returned from rest/nodes/variables

   properties = list of properties and values

'''

from .. item_base import Item_Base


class Variable_Base(Item_Base):

    def __init__(self, container, variable_info): 
        Item_Base.__init__(self,container,variable_info.id) # replaced once names are retrieved

        self.id = variable_info.id
        self.type = variable_info.type

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

    def set_value(self,value):
        path = ('vars/set/' + self.type + '/' + self.id + '/' + str(value))
        return self.send_request(path)        


