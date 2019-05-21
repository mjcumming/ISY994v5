#! /usr/bin/env python

'''

container for a collection of items

category = device, variable, program, scene

'''

import logging
logger = logging.getLogger(__name__)

#containter events = {'add','remove','property'}

class Item_Manager (object):

    def __init__(self, controller, category):
        self.controller = controller
        self.category = category

        self.list = {} # indexed by device(node) address

    def start(self):
        pass
       
    def send_request(self,path,query=None,timeout=None): 
        return self.controller.send_request(path,query,timeout)

    def websocket_event(self,event):
        pass

    def add(self,item,key):
        self.list [key] = item
        self.event (item,'add')

    def remove(self,key):
        item = self.list [key]
        del self.list [key]
        self.event (item,'remove')

    def get(self,key):
        return self.list [key]

    def property_change(self,item,property_,value): # called by the item to publish a change
        self.event(item,'property',property_,value)
    
    def event(self,item,event,*args): #publish event to controller
        print ('item event',self.category,item.name,event)
        #self.controller.item_event (self.category,item,event,args)
    
    
        

