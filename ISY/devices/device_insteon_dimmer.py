#! /usr/bin/env python


#Device: Kids Bathroom Vanity Light ; address 50 A 83 1 ; cat 1, sub_cat 32, version 69, parent 27840
#<node flag="128" nodeDefId="DimmerLampSwitch_ADV"><address>50 A 83 1</address><name>Kids Bathroom Vanity Light</name><parent type="3">27840</parent><type>1.32.69.0</type><enabled>true</enabled><deviceClass>0</deviceClass><wattage>0</wattage><dcPeriod>0</dcPeriod><startDelay>0</startDelay><endDelay>0</endDelay><pnode>50 A 83 1</pnode><property formatted="100%" id="ST" uom="100" value="255" /></node>

from .device_base import Device_Base

class Device_Insteon_Dimmer(Device_Base):

    def __init__(self, node):
        Device_Base.__init__(self,node)

        property_node = node.find('property')
        
        if 'value' in property_node.attrib:
            try:
                self.level = int(property_node.attrib['value'])
            except:
                self.level = None

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self,level):
        print ('set level to',level)
        self._level = level

    def process_websocket_event(self,event):
            #print ('device event')
            if event.control == 'ST':
                print ('device {}. changed status to {}'.format(event.node,event.action))
            elif event.control in ['DON','DOF']:
                print ('device {}. changed local control {}'.format(event.node,event.action))

