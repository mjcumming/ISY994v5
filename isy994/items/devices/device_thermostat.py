#! /usr/bin/env python


from .device_base import Device_Base



class Device_Thermostat(Device_Base):

    def __init__(self, container, name, address):
        Device_Base.__init__(self,container,'thermostat', name, address)

        self.add_property('temperature',0) 
        self.add_property('humidity',0) 
        self.add_property('coolsetpoint',0) 
        self.add_property('heatsetpoint',0) 
        self.add_property('mode','') 

    def set_level(self,level):
        pass

