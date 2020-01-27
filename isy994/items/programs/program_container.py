#! /usr/bin/env python


import xml.etree.ElementTree as ET
import traceback

from .. item_container import Item_Container
from .program_info import Program_Info 
from .program_base import Program_Base


import logging
logger = logging.getLogger(__name__)


class Program_Container (Item_Container):

    def __init__(self, controller):
        Item_Container.__init__(self,controller,'Program')

    def start(self):
        success,response = self.controller.send_request('programs/?subfolders=true')

        if success:
            try:
                root = ET.fromstring (response)        
                self.process_program_nodes (root)    
                self.items_retrieved = True
                return True

            except Exception as ex:
                logger.error('container error {}'.format(ex))
                traceback.print_exc()
        else:
            return False

    def process_program_nodes(self,root):
        for program in root.iter('program'):
            self.process_program_node(program)
                
    def process_program_node(self,node):
        program_info = Program_Info(node) # parse node XML

        if program_info.valid: # make sure we have the info we need
            program = Program_Base(self,program_info)
            self.add(program,program.id)
         
    def websocket_event(self,event):
        #print('Program event',event)
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
            program = self.get(id)
            if program:
                program.process_websocket_event (status,run_time,finish_time)
            else:
                logger.warning('Unable able to find program type id {}'.format(id))

