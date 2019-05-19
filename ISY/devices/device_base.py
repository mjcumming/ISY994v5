#! /usr/bin/env python

''' 

Base Device

Common to all elements returned from rest/nodes/devices

   properties = list of properties and values

'''



class Device_Base(object):

    def __init__(self, parent, device_info):
        self.parent = parent

        self.properties = {'status' : None} # list of properties key = property name, value = property value

        self.family = device_info.family
        self.category = device_info.category
        self.sub_category = device_info.sub_category
        self.version = device_info.version
        self.res = device_info.reserved
        self.address = device_info.address
        self.address_parts = device_info.address_parts
        self.name = device_info.name
        self.flag = device_info.flag
        self.parent_node_address = device_info.parent_node_address


    def __str__(self):
        return ("Device: {} ; address {} ; flag {}; cat {}, sub_cat {}, version {}, parent {}".format(self.name, self.address, self.flag, self.category, self.sub_category, self.version, self.parent_node_address))

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self,flag):
        self._flag = flag
        if flag & 16:
            self.set_property ('status','alert')
        else:
            self.set_property ('status','ready')
        
    def process_websocket_event(self,event):
        pass # classes to override

    def add_property(self, property_, value = None):
        self.properties [property_] = value

    def set_property(self, property_, value):
        self.properties [property_] = value
        self.parent.device_property_change(self,property_,value) 
 
    def get_property(self, property_):
        return self.properties [property_] 

    def send_request(self,path,query=None): 
        return self.parent.send_request(path,query)