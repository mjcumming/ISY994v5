#! /usr/bin/env python

""" 

Base Device

Common to all elements returned from rest/nodes/devices

   properties = list of properties and values

"""


class Device_ZWave_Base(object):
    def __init__(self, device_info):
        self.family = device_info.family
        self.category = device_info.category
        self.sub_category = device_info.sub_category
        self.version = device_info.version
        self.res = device_info.reserved
        # self.address = device_info.address
        self.address_parts = device_info.address_parts
        self.flag = device_info.flag
        self.devtype_cat = device_info.devtype_cat
        # self.container_node_address = device_info.container_node_address

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, flag):
        self._flag = flag
        if flag & 16:
            self.set_property("status", "alert")
        else:
            self.set_property("status", "ready")
