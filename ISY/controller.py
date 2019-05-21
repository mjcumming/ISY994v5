#! /usr/bin/env python

import time
import datetime

from items.devices.device_manager import Device_Manager 
from items.scenes.scene_manager import Scene_Manager 
from items.variables.variable_manager import Variable_Manager 
from items.programs.program_manager import Program_Manager 

from network.http_client import HTTP_Client
from network.websocket_client import Websocket_Client
from network.discover import Discover

import logging
logger = logging.getLogger(__name__)

#event categores controller, device, scene, variable, program


class Controller(object):

    def __init__(self,address=None,port=None,username='admin',password='admin',use_https=False,event_handler=None):
        if address == None:
            discover = Discover()
            controller_list = discover.start()
            if len(controller_list) > 0:
                address = controller_list[0]

        if address is None:
            print('no controller found')

        self.event_handlers = []
        if event_handler is not None:
            self.event_handlers.append(event_handler)

        self.http_client = HTTP_Client (address,port,username,password,use_https)

        self.device_manager = Device_Manager(self)
        self.scene_manager = Scene_Manager(self)
        self.variable_manager = Variable_Manager(self)
        self.program_manager = Program_Manager(self)

        self.last_heartbeat = None

        self.start()

        self.websocket_client = Websocket_Client(self,address,port,username,password,False)

    def start(self):
        self.device_manager.start() # need to check for result
        self.scene_manager.start() # need to check for result
        self.variable_manager.start() # need to check for result
        self.program_manager.start() # need to check for result

    def device_event(self,device,event,*args):
        print ('Device event from {}, address {}, event {} args {}'.format (device.name,device.address,event,args))   
        self.publish_event ('device',device,event,args)
        self.scene_manager.device_event (device)   #used to determine "state" of a scene
            
    def scene_event(self,scene,event,*args):
        self.publish_event ('scene',scene,event,args)
        print ('Scene event from {}, address {}, event {} args {}'.format (scene.name,scene.address,event,args))      
            
    def variable_event(self,variable,event,*args):
        self.publish_event ('variable',variable,event,args)
        print ('Variable event from {}, index {}, event {} args {}'.format (variable.name,variable.get_index(),event,args))      
            
    def program_event(self,program,event,*args):
        self.publish_event ('program',program,event,args)
        print ('Program event from {}, id {}, event {} args {}'.format (program.name,program.id,event,args))      

    def publish_event(self,category,item,event,*args):
        for event_handler in self.event_handlers:
            try:
                event_handler (category,item,event,args)
            except Exception as ex:
                logger.error('Event handler Error {}'.format(ex))
            
    def send_request(self,path,query=None,timeout=None): 
        return self.http_client.request(path,query,timeout)

    def websocket_connected(self,connected): #True websocket connected, False, no connection
        pass #TBD

    def websocket_event(self,event): #process websocket event
        #print ('WS Event {}'.format(event))

        if event.address is not None: #event from a device/node
            self.device_manager.websocket_event (event)

        if event.control == '_0': # heartbeat
            self.process_heartbeat(event)

        elif event.control == '_1': # trigger
            if event.action == '0': #program
                self.program_manager.websocket_event (event)
            elif event.action == '6': # variable change
                self.variable_manager.websocket_event (event)

        elif event.control == '_5': # system status
            self.process_system_status(event)

    def process_heartbeat(self,event):
        self.last_heartbeat = datetime.datetime.now()

    def process_system_status(self,event):
        if event.action =='0': #idle
            pass
        elif event.action == '1':#busy
            pass 





url = '192.168.1.213'


if __name__ == "__main__":

    try:
        c = Controller(url,username='admin',password='admin')
        time.sleep(2)
        #device = c.device_manager.get_device('42 C8 99 1')
        #print ('got device',device)

        #scene = c.scene_manager.get_scene('25770')
        #print ('got scene',scene)

        #program = c.program_manager.get_program ('0022')

        while True:
            time.sleep(2)
            #device.set_level (0)
            #scene.turn_on()
            #program.run()
            time.sleep(2)
            #scene.turn_off()
            #device.set_level (100)
            #program.run_else()

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
