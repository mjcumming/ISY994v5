#! /usr/bin/env python

import xml.etree.ElementTree as ET
import traceback

from ..item_container import Item_Container

from .device_info import Device_Info

from .insteon_device_manager import get_insteon_device_class



import logging
logger = logging.getLogger(__name__)


class Device_Container (Item_Container):

    def __init__(self, controller):
        Item_Container.__init__(self,controller,'Device')

    def start(self):
        success,response = self.send_request('nodes/devices')

        if success and response.status_code == 200:
            try:
                root = ET.fromstring (response.content)        
                self.process_device_nodes (root)    
                self.items_retrieved = True
                return True
            
            except Exception as ex:
                    logger.error('container error {}'.format(ex))
                    traceback.print_exc()
        else:
            return False

    def process_device_nodes(self,root):
        for device in root.iter('node'):
            self.process_device_node(device)
                
    def process_device_node(self,node):
        device_info = Device_Info(node) # parse node XML
        #print('process node',device_info.valid,device_info)

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
                device_class = get_insteon_device_class (device_info)
                if device_class is not None:
                    device = device_class(self,device_info)
                    self.add(device,device.address)
                else:
                    logger.warn('No device class for {}'.format(device_info))

            
         
    def websocket_event(self,event):
        #print('Device event',event)
        device = self.get(event.address)
        if device is not None:
            device.process_websocket_event(event)

    
    
        

