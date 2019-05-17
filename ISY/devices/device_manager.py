#! /usr/bin/env python

import xml.etree.ElementTree as ET

from .device_insteon_dimmer import Device_Insteon_Dimmer
from .device_insteon_switch import Device_Insteon_Switch

device_classes = {
    '1' : Device_Insteon_Dimmer,
    '2' : Device_Insteon_Switch,
}

class Device_Manager (object):

    def __init__(self, controller):

        self.device_list = {} # indexed by device(node) address

        self.controller = controller

    def process_node(self,node):
        _type = node.find('type')
        address = node.find('address')
        address_parts = address.text.split(' ')

        if _type is None: #missing 
            print ('missing node type for node {}'.format(node))
            return False

        types = _type.text.split('.')
        device_category = types [0]

        #override device cat for keypadlinc dimmer buttons and change to switch type devices
        if device_category == '1' and address_parts [3] != '1': # maybe use node flag
            device_category = '2'

        #create device
        if device_category in device_classes:
            device_class = device_classes [device_category]

            device = device_class(node)

            print(device)

    def add_device(self,device):
        self.device_list [device.address] = device

    
        

