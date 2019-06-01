#! /usr/bin/env python


from .device_base import Device_Base


class Device_Speed_Controller(Device_Base):

    def __init__(self, container, name , address, speeds=['off','low','medium','high']):
        Device_Base.__init__(self,container,'speed_controller',name, address)

        self.speeds = speeds

        self.add_property('speed','off') 

    def set_speed(self,speed):
        pass

