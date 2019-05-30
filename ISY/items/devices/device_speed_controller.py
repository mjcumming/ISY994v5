#! /usr/bin/env python


from .device_base import Device_Base


class Device_Speed_Controller(Device_Base):

    def __init__(self, container,speeds=['off','low','medium','high']):
        Device_Base.__init__(self,container,'speed_controller')

        self.speeds = speeds

        self.add_property('speed','unknown') 

    def set_speed(self,speed):
        pass

