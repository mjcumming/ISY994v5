#! /usr/bin/env python


from .device_base import Device_Base


class Device_Notification(Device_Base):
    def __init__(self, container, name, address):
        Device_Base.__init__(self, container, "notification", name, address)

        self.add_property("notification", None)
        self.add_property("batterylevel", 0)

