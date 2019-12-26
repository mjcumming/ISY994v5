#! /usr/bin/env python


from .device_base import Device_Base



class Device_Thermostat(Device_Base):

    def __init__(self, container, name, address):
        Device_Base.__init__(self,container,'thermostat', name, address)

        self.add_property('temperature',0) 
        self.add_property('humidity',0) 
        self.add_property('coolsetpoint',0) 
        self.add_property('heatsetpoint',0) 
        self.add_property('systemmode',0) 
        self.add_property('fanmode',0) 

    def set_mode (self,mode):
        pass
 
    def set_heatsetpoint (self,setpoint):
        pass
 
    def set_coolsetpoint (self,setpoint):
        pass

    def set_fanmode (self,mode):
        pass