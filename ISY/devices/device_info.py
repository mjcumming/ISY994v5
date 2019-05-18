#! /usr/bin/env python

import xml.etree.ElementTree as ET

# process a node and assemble the info to build a device

class Device_Info(object):

    def __init__(self,node):

        self.valid = False

        try:
            self.family = '1' # default to insteon
            if node.find('family'): # insteon does not set node family
                self.family = node.find('family').text

            type_ = node.find('type')
            self.type = type_.text
            types = type_.text.split('.')
            self.category = types [0]    
            self.sub_category = types [1]    
            self.version = types [2]    
            self.reserved = types [3] 

            address = node.find('address')
            self.address = address.text
            self.address_parts = address.text.split(' ')

            name = node.find('name')
            self.name = name.text

            flag = node.get ('flag')
            self.flag = int(flag) 

            types = type_.text.split('.')
            device_category = types [0]

            parent_node = node.find('parent')
            self.parent_node_address = parent_node.text  
        
            property_node = node.find('property')
            if 'value' in property_node.attrib:
                self.property_value = property_node.attrib['value']
            else:
                self.property_value = None

            self.valid = True
        except:
            pass

    def __repr__(self):
        return 'Device: Name {} Address {}, Family {}, Type {}'.format(self.name,self.address,self.family,self.type)
    