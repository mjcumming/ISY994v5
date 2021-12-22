#! /usr/bin/env python

import traceback
from datetime import datetime
import xml.etree.ElementTree as ET
import threading

""" 

Base Device

Common to all elements returned from rest/nodes/devices

device_type = switch,dimmer,contact,...

having a common device types eliminates the need to know the underlying technology being used

"""


from ...item_base import Item_Base


class Device_Base(Item_Base):
    def __init__(self, container, device_type, name, address):
        Item_Base.__init__(self, container, name)

        self.device_type = device_type
        self.address = address

        self.last_command_path = None # last command we sent to the device
        self.last_command_time = None # time last command sent
        self.last_command_retry_interval = 10 # if device status changes time to allow for retry

        self.add_property("communication_ok",True) # False means in a failed state
        self.add_property("communication_error_count",0) # number of time there is a failed communication
        self.add_property("communication_error_state_count",0) # number of time the device enters an alert state
        self.add_property("communication_requests",0) # number of time the device we senda request to a device

    def __str__(self):
        return "Device {}, type {}, ID {}".format(
            self.name, self.device_type, self.address
        )

    def get_identifier(self):
        return self.address
    
    def send_request(self, path, timeout=None):
        self.set_property("communication_requests",self.get_property("communication_requests")+1)
        if self.get_property("communication_ok") is False:
            self.set_property("communication_error_count",self.get_property("communication_error_count")+1)

        self.last_command_path = path
        self.last_command_time = datetime.now()
        success,response = Item_Base.send_request(self,path,timeout)
        return success,response

    def process_websocket_event(self, event):
        if event.control == "_3":
            if event.action == "NE": # comms error
                self.communication_failure()
            elif event.action == "CE": # comms error clear
                self.communications_restored()

    def get_status(self): #isy status for node
        path = "status/" + self.address 
        success, response = self.send_request(path)

        if success:  # and response.status == 200:
            try:
                root = ET.fromstring(response)
                node = (root.find(".//property[@id='ERR']"))

                if int(node.attrib ["value"]) == 0:
                    self.communications_restored()
                elif int(node.attrib ["value"]) > 0:
                    self.set_property ('status','alert',True)  #always publish
                    self.communications_failed()

            except Exception:
                traceback.print_exc()

        return success, response

    def communication_failure(self): # called when we receive a websocket event with a NE comm error
        self.set_property ('status','alert')
        self.set_property("communication_error_state_count",self.get_property("communication_error_state_count")+1)
        self.set_property("communication_ok",False) 

        if self.last_command_path is not None:
            if (datetime.now()-self.last_command_time).seconds <= self.last_command_retry_interval:
                def send_request():
                    self.send_request(self.last_command_path) # do it twice!
                    self.send_request(self.last_command_path)

                # **** not sure this is a good way to do this but cannot call send request in the websocket call back
                th = threading.Thread(target=send_request)
                th.start()                

    def communications_failed(self): # called when device status returns device in comm failed state
        self.set_property ('status','alert')
        self.set_property("communication_error_state_count",self.get_property("communication_error_state_count")+1)
        self.set_property("communication_ok",False) 
        pass

    def communications_restored(self):
        self.set_property ('status','ready')
        self.set_property("communication_ok",True) 
