#! /usr/bin/env python


from .device_base import Device_Base

class Device_Insteon_Switch(Device_Base):

    def __init__(self, node):
        Device_Base.__init__(self,node)

        property_node = node.find('property')
        
        if 'value' in property_node.attrib:
            try:
                self.onoff = int(property_node.attrib['value']) > 0
            except:
                self.onoff = None

    @property
    def onoff(self):
        return self._onoff #True = on

    @onoff.setter
    def onoff(self,onoff):
        print ('set onoff',onoff)
        self._onoff = onoff