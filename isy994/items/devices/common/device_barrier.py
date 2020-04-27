#! /usr/bin/env python


from .device_base import Device_Base


class Device_Barrier(Device_Base):
    def __init__(self, container, name, address):
        Device_Base.__init__(self, container, "barrier", name, address)

        self.add_property("barrier", 0)
        self.add_property("state", None)

