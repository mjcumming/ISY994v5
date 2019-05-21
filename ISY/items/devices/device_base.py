#! /usr/bin/env python

''' 

Base Device

Common to all elements returned from rest/nodes/devices

device_type = switch,dimmer,contact

'''

from .. item_base import Item_Base


class Device_Base(Item_Base):

    def __init__(self, container, device_type, device_info):
        Item_Base.__init__(self,container)

        self.device_type = device_type

