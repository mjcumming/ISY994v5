#! /usr/bin/env python

import xml.etree.ElementTree as ET
import time

from devices.device_manager import Device_Manager 
from connection import Connection
from websocket_client import Websocket_Client



class Controller(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):

        self._connection = Connection (address,port,username,password,use_https)

        self.device_manager = Device_Manager(self)

        self.start()

        self.websocket_client = Websocket_Client(self,address,port,username,password,False)

    def start(self):
        self.add_devices()

    def add_devices(self):
        response = self.send_request('nodes/devices')

        if response.status_code == 200:
            root = ET.fromstring (response.content)        
            self.device_manager.process_device_nodes (root)       

    def device_event(self,device,event,*args):
        print ('Device event from {}, address {}, event {} args {}'.format (device.name,device.address,event,args))      
            
    def send_request(self,path,query=None): 
        return self._connection.request(path,query)

    def websocket_connected(self,connected): #True websocket connected, False, no connection
        pass #TBD

    def websocket_event(self,event): #process websocket event

        if event.address is not None: #event from a device/node
            self.device_manager.websocket_event (event)

        if event.control == '_0': # heartbeat
            pass

        






url = '192.168.1.213'


if __name__ == "__main__":

    try:
        c = Controller(url,username='admin',password='admin')
        time.sleep(2)
        device = c.device_manager.get_device('42 C8 99 1')
        print ('got device',device)

        while True:
            time.sleep(2)
            device.set_level (0)
            time.sleep(2)
            device.set_level (100)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
