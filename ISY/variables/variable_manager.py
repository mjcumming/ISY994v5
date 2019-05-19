#! /usr/bin/env python

import xml.etree.ElementTree as ET

from .variable_info import Variable_Info
from .variable_name import Variable_Name

from .variable_integer import Variable_Integer
from .variable_state import Variable_State

variable_classes = {
    '1' : Variable_Integer,
    '2' : Variable_State,
}

variable_events = {'add','remove','property'}

class Variable_Manager (object):

    def __init__(self, controller):
        self.controller = controller

        self.variable_list = {} # indexed by variable type.id

    def start(self):
        success = True

        variable_list_response = self.controller.send_request('vars/get/1') # get integer vars
        variable_name_response = self.controller.send_request('vars/definitions/1') # get integer vars

        if variable_list_response.status_code == 200 and variable_name_response.status_code == 200:
            list_root = ET.fromstring (variable_list_response.content)        
            name_root = ET.fromstring (variable_name_response.content)        
            self.process_variable_nodes (list_root,name_root)       
        else:
            success = False

        variable_list_response = self.controller.send_request('vars/get/2') # get state vars
        variable_name_response = self.controller.send_request('vars/definitions/2') # get state vars

        if variable_list_response.status_code == 200 and variable_name_response.status_code == 200:
            list_root = ET.fromstring (variable_list_response.content)        
            name_root = ET.fromstring (variable_name_response.content)        
            self.process_variable_nodes (list_root,name_root)       
        else:
            success = False

    def process_variable_nodes(self,list_root,name_root):
        for node in list_root.iter('var'):
            variable_info = Variable_Info(node)

            if variable_info.valid: # make sure we have the info we need
                variable_class = variable_classes [variable_info.type]
                variable = variable_class(self,variable_info)

                #find name
                for node in name_root.iter('e'):
                    variable_name = Variable_Name (node)

                    if variable_name.valid and variable_name.id == variable.id:
                        variable.name = variable_name.name

                self.add_variable(variable)
         
    def send_request(self,path,query=None): 
        return self.controller.send_request(path,query)

    def websocket_event(self,event):
        var = event.event_info_node.find('var')
        variable_id = var.attrib ['id']
        variable_type = var.attrib ['type']

        index = variable_type+':'+variable_id

        variable = self.get_variable(index)
        variable.process_websocket_event(event)

    def add_variable(self,variable):
        self.variable_list [variable.get_index()] = variable
        self.variable_event (variable,'add')

    def remove_variable(self,index):
        variable = self.variable_list [index]
        del self.variable_list [index]
        self.variable_event (variable,'remove')

    def get_variable(self,index):
        return self.variable_list [index]

    def variable_property_change(self,variable,property_,value):
        self.variable_event(variable,'property',property_,value)
    
    def variable_event(self,variable,event,*args):
        self.controller.variable_event (variable,event,args)

    def get_device(self,index):
        return self.controller.device_manager.get_device(index)
    
        

