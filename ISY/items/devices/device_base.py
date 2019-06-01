#! /usr/bin/env python

''' 

Base Device

Common to all elements returned from rest/nodes/devices

device_type = switch,dimmer,contact

'''


from .. item_base import Item_Base


class Device_Base(Item_Base):

    def __init__(self, container, device_type, name):
        Item_Base.__init__(self,container, name)

        self.device_type = device_type

    def __str__(self):
        return ('Device {}, type {}, ID {}'.format(self.name,self.device_type,self.address))

