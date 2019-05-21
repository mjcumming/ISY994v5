#! /usr/bin/env python

import xml.etree.ElementTree as ET

from .. item_manager import Item_Manager

from .device_info import Device_Info

from .device_insteon_dimmer import Device_Insteon_Dimmer
from .device_insteon_switch import Device_Insteon_Switch

insteon_device_classes = {
    '1' : Device_Insteon_Dimmer,
    '2' : Device_Insteon_Switch,
}

import logging
logger = logging.getLogger(__name__)


class Device_Manager (Item_Manager):

    def __init__(self, controller):
        Item_Manager.__init__(controller,'Device')

    def start(self):
        response = self.controller.send_request('nodes/devices')

        if response.status_code == 200:
            root = ET.fromstring (response.content)        
            self.process_device_nodes (root)    

            return True
        else:
            return False

    def process_device_nodes(self,root):
        for device in root.iter('node'):
            self.process_device_node(device)
                
    def process_device_node(self,node):
        device_info = Device_Info(node) # parse node XML

        if device_info.valid: # make sure we have the info we need
            ''' device family
            	0 = Default (core driver implementation e.g. Insteon, UPB)
				1 = Insteon products
				2 = UPB Products
				3 = RCS Products
				4 = ZWave products
				5 = Auto DR (for groups)
				6 = Generic (for groups)
				7 = UDI Products
				8 = Brultech Products
				9 = NCD Products
            '''
            
            if device_info.family == '1': #insteon devices
                #override device cat for keypadlinc dimmer buttons and change to switch type devices
                if device_info.category == '1' and device_info.address_parts [3] != '1': # maybe use node flag
                    device_info.category = '2'

                #create device
                if device_info.category in insteon_device_classes:
                    device_class = insteon_device_classes [device_info.category]

                    device = device_class(self,device_info)
                    self.add(device,device.address)
         
    def websocket_event(self,event):
        print('Device event',event)
        device = self.get_device(event.address)
        device.process_websocket_event(event)

    def device_property_change(self,device,property_,value): # called by the device to publish a change
        self.device_event(device,'property',property_,value)
    
    def device_event(self,device,event,*args): #publish event
        self.controller.device_event (device,event,args)
    
    
        

