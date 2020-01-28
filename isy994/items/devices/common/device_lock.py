#! /usr/bin/env python


from .device_base import Device_Base


class Device_Lock(Device_Base):
    def __init__(self, container, name, address):
        Device_Base.__init__(self, container, "lock", name, address)

        self.add_property("batterylevel", 0)
        self.add_property("state", 0)
        self.add_property("error", 0)
        self.add_property("usernumber", 0)

    def lock(self):
        pass

    def unlock(self):
        pass
