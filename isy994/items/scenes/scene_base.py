#! /usr/bin/env python

''' 

Base Scene

Common to all elements returned from rest/nodes/scenes

TBD - may need to change - scene_base and scene_inteon based on insteon only setup

'''

from .. item_base import Item_Base

class Scene_Base(Item_Base):

    def __init__(self, container, scene_info):
        Item_Base.__init__(self,container,scene_info.name)

        self.address = scene_info.address
        self.flag = scene_info.flag
        self.id = scene_info.id
        self.family = scene_info.family

        self.primary_node = scene_info.primary_node

        self.device_group = scene_info.device_group

        self.controllers = scene_info.controllers
        self.responders = scene_info.responders

    def __str__(self):
        return ("Scene: {} ; address {} ; flag {}; id {}".format(self.name, self.address, self.flag, self.id))

    def device_event(self,device): #device event, process and see if we are interested
        pass # subclasses to provide

    def get_identifier(self):
        return self.address       
        