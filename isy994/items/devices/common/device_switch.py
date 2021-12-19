#! /usr/bin/env python


from .device_base import Device_Base


class Device_Switch(Device_Base):
    def __init__(self, container, name, address):
        Device_Base.__init__(self, container, "switch", name, address)

        self.add_property("onoff", "off")

    def turn_on(self):
        pass

    def turn_off(self):
        pass

