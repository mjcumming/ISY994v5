#! /usr/bin/env python



from .device_base import Device_Base


class Device_Contact (Device_Base):

    def __init__(self, container,name,address):
        Device_Base.__init__(self,container,'contact',name,address)

        self.add_property('contact',None)



