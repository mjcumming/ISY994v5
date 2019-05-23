#! /usr/bin/env python

import xml.etree.ElementTree as ET

import traceback

# process a node and assemble the info to build a device


''' zwave node....
<nodeInfo>
<node flag="0">
<address>ZW002_143</address>
<name>ZW 002 Energy Meter</name>
<family>4</family>
<type>4.33.1.0</type>
<enabled>true</enabled>
<deviceClass>0</deviceClass>
<wattage>0</wattage>
<dcPeriod>0</dcPeriod>
<startDelay>0</startDelay>
<endDelay>0</endDelay>
<pnode>ZW002_1</pnode>
<sgid>143</sgid>
<devtype>
<gen>4.33.1</gen>
<mfg>134.2.9</mfg>
<cat>143</cat>
</devtype>
<ELK_ID>I16</ELK_ID>
<property id="ST" value="91289" formatted="912.89 Watts" uom="73" prec="2"/>
</node>
<properties>
<property id="ST" value="91289" formatted="912.89 Watts" uom="73" prec="2"/>
<property id="TPW" value="31765" formatted="317.65 kWh" uom="33" prec="2"/>
</properties>
</nodeInfo>
'''

class Device_Info(object):

    def __init__(self,node):

        self.node = node

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
            self.node_dev_id = node.get('nodeDefId')

            #container_node = node.find('container')
            #self.container_node_address = container_node.text  
        
            property_node = node.find('property')
            if 'value' in property_node.attrib:
                self.property_value = property_node.attrib['value']
            else:
                self.property_value = None

            self.valid = True
        
        except Exception as ex:
                traceback.print_exc()       

    def __repr__(self):
        return 'Device: Name {} Address {}, Family {}, Type {}, Def ID {}'.format(self.name,self.address,self.family,self.type,self.node_dev_id)
    