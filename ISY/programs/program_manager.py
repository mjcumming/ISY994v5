#! /usr/bin/env python

import xml.etree.ElementTree as ET

import logging
logger = logging.getLogger(__name__)

from .program_info import Program_Info

from .program_base import Program_Base

program_events = {'add','remove','property'}

class Program_Manager (object):

    def __init__(self, controller):
        self.controller = controller

        self.program_list = {} # indexed by program(node) id

    def start(self):
        response = self.controller.send_request('programs','subfolders=true')

        if response.status_code == 200:
            root = ET.fromstring (response.content)        
            self.process_program_nodes (root)    

            return True
        else:
            return False

    def process_program_nodes(self,root):
        for program in root.iter('program'):
            self.process_program_node(program)
                
    def process_program_node(self,node):
        program_info = Program_Info(node) # parse node XML

        if program_info.valid: # make sure we have the info we need
            program = Program_Base(self,program_info)
            self.add_program(program)
         
    def send_request(self,path,query=None,timeout=None): 
        return self.controller.send_request(path,query,timeout)

    def websocket_event(self,event):
        #print('Program event',event)
        try:
            id = event.event_info_node.find('id').text.zfill(4) 

            status = None
            run_time = None
            finish_time = None
            
            if event.event_info_node.find('s') is not None:
                status = int(event.event_info_node.find('s').text )

            if event.event_info_node.find('r') is not None:
                run_time = event.event_info_node.find('r').text 

            if event.event_info_node.find('f') is not None:
                finish_time = event.event_info_node.find('f').text 

            if status and run_time and finish_time:
                program = self.get_program(id)
                program.process_websocket_event (status,run_time,finish_time)

        except Exception as e: 
            print(e)



        #program = self.get_program(event.id)
        #program.process_websocket_event(event)

    def add_program(self,program):
        self.program_list [program.id] = program
        self.program_event (program,'add')

    def remove_program(self,id):
        program = self.program_list [id]
        del self.program_list [id]
        self.program_event (program,'remove')

    def get_program(self,id):
        return self.program_list [id]

    def program_property_change(self,program,property_,value): # called by the program to publish a change
        self.program_event(program,'property',property_,value)
    
    def program_event(self,program,event,*args): #publish event
        self.controller.program_event (program,event,args)
    
    
        

