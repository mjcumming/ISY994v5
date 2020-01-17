#! /usr/bin/env python

import time
import traceback
import threading 
from datetime import datetime
from datetime import timedelta

from .items.devices.device_container import Device_Container 
from .items.scenes.scene_container import Scene_Container 
from .items.variables.variable_container import Variable_Container 
from .items.programs.program_container import Program_Container 
from .items.controller.controller_container import Controller_Container 

from .network.http_client import HTTP_Client
from .network.websocket_client import Websocket_Client
from .network.discover import Discover

from .support.repeating_timer import Repeating_Timer

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
            logger.error('No controller address found')
            quit()

        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.use_https= use_https

        self.event_handlers = []
        if event_handler is not None:
            self.event_handlers.append(event_handler)

        self.controller_container = Controller_Container(self)
        self.device_container = Device_Container(self)
        self.scene_container = Scene_Container(self)
        self.variable_container = Variable_Container(self)
        self.program_container = Program_Container(self)

        self.last_heartbeat = None
        self.heartbeat_interval = 30 # set below by data from controller, needed her for watchdog if no initial connection

        self.websocket_client = None

        self.controller_container.start()        
        
        self.start()

        self.watch_dog_timer = Repeating_Timer(30)
        self.watch_dog_timer.add_callback(self.watch_dog_check)

    def start(self):
        self.http_client = HTTP_Client (self.address,self.port,self.username,self.password,self.use_https)

        if self.get_controller_items () is True:
            self.process_controller_event('status','ready')
            self.connect_websocket()
        else:
            self.process_controller_event('status','error')
            self.retry_start(10)

    def retry_start(self,delay_seconds):
        def restart ():
            self.start()

        self.restart_timer = threading.Timer(delay_seconds, restart) 
        self.restart_timer.start()
        
    def get_controller_items(self):
        success = True
        self.process_controller_event('status','init')        

        if self.device_container.items_retrieved is False:
            if self.device_container.start() is False:
                success = False

        if self.scene_container.items_retrieved is False:
            if self.scene_container.start() is False:
               success = False  

        if self.variable_container.items_retrieved is False:
            if self.variable_container.start() is False:
                success = False 
        
        if self.program_container.items_retrieved is False:
            if self.program_container.start() is False:
                success = False
        
        return success

    def connect_websocket(self):
        if self.websocket_client is None:
            self.websocket_client = Websocket_Client(self,self.address,self.port,self.username,self.password,False)

    def container_event(self,container,item,event,*args):
        #print ('Event {} from .{}: {} {}'.format(item.name,container.container_type,item,args))
        self.publish_container_event(container,item,event,*args)

        if container.container_type == 'Device':# propagate to scene container to see if we should update
            self.scene_container.device_event(item)

    def publish_container_event(self,container,item,event,*args):
        for event_handler in self.event_handlers:
            try:
                event_handler (container,item,event,*args)
            except Exception as ex:
                logger.error('Event handler Error {}'.format(ex))
                traceback.print_exc()
            
    def send_request(self,path,query=None,timeout=None): 
        success,response = self.http_client.request(path,query,timeout)
        if success:
            self.process_controller_event('http','connected')
        else:
            self.process_controller_event('http','error')
        return success, response

    def websocket_connected(self,connected): #True websocket connected, False, no connection
        if connected:
            self.process_controller_event('websocket','connected')
        else:
            self.process_controller_event('websocket','disconnected')

    def websocket_event(self,event): #process websocket event
        #print ('WS Event {}'.format(event))
        try:

            if event.address is not None: #event from .a device/node
                self.device_container.websocket_event (event)

            if event.control == '_0': # heartbeat
                self.process_heartbeat(event)

            elif event.control == '_1': # trigger
                if event.action == '0': #program
                    self.program_container.websocket_event (event)
                elif event.action == '6': # variable change
                    self.variable_container.websocket_event (event)

            elif event.control == '_5': # system status
                self.process_system_status(event)

        except Exception as ex:
                logger.error('websocket handler Error {}'.format(ex))
                traceback.print_exc()

    def process_controller_event(self,property_,value):
        controller = self.controller_container.get('controller')
        controller.set_property(property_,value)

    def process_heartbeat(self,event):
        self.last_heartbeat = datetime.now()#.strftime("%m/%d/%Y, %H:%M:%S")
        self.process_controller_event('heartbeat',self.last_heartbeat)
        self.heartbeat_interval = int(event.action)

    def process_system_status(self,event):
        if event.action =='0': #idle
            self.process_controller_event('state','idle')
        elif event.action == '1':#busy
            self.process_controller_event('state','busy')

    def watch_dog_check(self):
        if self.last_heartbeat + timedelta (seconds=self.heartbeat_interval) < datetime.now():
            logger.warn('Watchdog timer triggered. Restarting')
            self.start()
        self.websocket_client._ws.keep_running=False