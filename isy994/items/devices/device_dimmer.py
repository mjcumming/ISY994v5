#! /usr/bin/env python


from .device_base import Device_Base


class Device_Dimmer(Device_Base):

    def __init__(self, container, name, address):
        Device_Base.__init__(self,container,'dimmer', name, address)

        self.add_property('level',0) #in percent

    def set_level(self,level):
        pass

