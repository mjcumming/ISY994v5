#! /usr/bin/env python

''' 

Base Device

Common to all elements returned from rest/nodes/devices

address
name
pnode
parent type
deviceClass


'''


class Device_Base(object):

    address = None,
    name = None,
    flag = None,
    category = None,
    sub_category = None,
    version = None,
    reserved = None,
    parent_node_address = None,
    error_state = False, # True, device in error state

    def __init__(self, node):
        self.process_node (node)

    def __str__(self):
        return ("Device: {} ; address {} ; flag {}; cat {}, sub_cat {}, version {}, parent {}".format(self.name, self.address, self.flag, self.category, self.sub_category, self.version, self.parent_node_address))

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self,flag):
        self._flag = flag
        if flag & 16:
            self.error_state == True
        else:
            self.error_state == False
        
    def process_node(self,node):
        flag = node.get ('flag')
        name = node.find('name')
        address = node.find('address')
        _type = node.find('type')
        parent_node = node.find('parent')

        if flag is None or name is None or address is None or _type is None or parent_node is None: #missing elements
            print ('missing data', flag, name, address, _type, parent_node)
            return False

        self.address = address.text
        self.name = name.text
        types = _type.text.split('.')
        self.category = types [0]    
        self.sub_category = types [1]    
        self.version = types [2]    
        self.reserved = types [3]  
        self.parent_node_address = parent_node.text  

        self.flag = int(flag) # flag 144, x90 seen when device in error - maybe use 1001 0000  1000 0000‬

    def process_websocket_event(self,event):
        pass # classes to override

 