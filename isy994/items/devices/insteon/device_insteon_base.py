#! /usr/bin/env python

""" 

Base Device

Common to all elements returned from rest/nodes/devices

   properties = list of properties and values

"""


from ..common.device_base import Device_Base


class Device_Insteon_Base(object):
    def __init__(self, device_info):
        self.family = device_info.family
        self.category = device_info.category
        self.sub_category = device_info.sub_category
        self.version = device_info.version
        self.res = device_info.reserved
        # self.address = device_info.address
        self.address_parts = device_info.address_parts
        self.flag = device_info.flag
        # self.container_node_address = device_info.container_node_address

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, flag):
        self._flag = flag
        if flag & 16:
            self.set_property("status", "alert")# pylint: disable=no-member
        else:
            self.set_property("status", "ready")# pylint: disable=no-member

    def beep(self): #not all insteon devices
        path = "nodes/" + self.address + "/cmd/BEEP"# pylint: disable=no-member
        return self.send_request(path)# pylint: disable=no-member

    def query(self): #no value returns, generates a websocket event if value is changed
        path = "nodes/" + self.address + "/cmd/QUERY"# pylint: disable=no-member
        return self.send_request(path)# pylint: disable=no-member        