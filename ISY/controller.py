#! /usr/bin/env python

import xml.etree.ElementTree as ET
import time

from devices.device_manager import Device_Manager 
from scenes.scene_manager import Scene_Manager 
from variables.variable_manager import Variable_Manager 

from connection import Connection
from websocket_client import Websocket_Client



class Controller(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):

        self._connection = Connection (address,port,username,password,use_https)

        self.device_manager = Device_Manager(self)
        self.scene_manager = Scene_Manager(self)
        self.variable_manager = Variable_Manager(self)

        self.start()

        self.websocket_client = Websocket_Client(self,address,port,username,password,False)

    def start(self):
        self.device_manager.start() # need to check for result
        self.scene_manager.start() # need to check for result
        self.variable_manager.start() # need to check for result

    def device_event(self,device,event,*args):
        print ('Device event from {}, address {}, event {} args {}'.format (device.name,device.address,event,args))   
        self.scene_manager.device_event (device)   
            
    def scene_event(self,scene,event,*args):
        print ('Scene event from {}, address {}, event {} args {}'.format (scene.name,scene.address,event,args))      
            
    def variable_event(self,variable,event,*args):
        print ('Variable event from {}, index {}, event {} args {}'.format (variable.name,variable.get_index(),event,args))      
            
    def send_request(self,path,query=None): 
        return self._connection.request(path,query)

    def websocket_connected(self,connected): #True websocket connected, False, no connection
        pass #TBD

    def websocket_event(self,event): #process websocket event

        if event.address is not None: #event from a device/node
            self.device_manager.websocket_event (event)

        if event.control == '_0': # heartbeat
            pass

        elif event.control == '_1': # trigger
            if event.action == '6': # variable change
                self.variable_manager.websocket_event (event)

        elif event.control == '_5': # system status
            pass

        






url = '192.168.1.213'


if __name__ == "__main__":

    try:
        c = Controller(url,username='admin',password='admin')
        time.sleep(2)
        #device = c.device_manager.get_device('42 C8 99 1')
        #print ('got device',device)

        scene = c.scene_manager.get_scene('25770')
        print ('got scene',scene)

        while True:
            time.sleep(2)
            #device.set_level (0)
            #scene.turn_on()
            time.sleep(2)
            #scene.turn_off()
            #device.set_level (100)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
