#! /usr/bin/env python


from .device_base import Device_Base


class Device_Speed_Controller(Device_Base):

    def __init__(self, container):
        Device_Base.__init__(self,container,'speed_controller')

        self.add_property('speed',0) #in percent

    def set_level(self,speed):
        pass

