#! /usr/bin/env python

import traceback

import xml.etree.ElementTree as ET

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

    def __str__(self):
        return "Device {}, type {}, ID {}".format(
            self.name, self.device_type, self.address
        )

    def get_identifier(self):
        return self.address
    
    def send_request(self, path, timeout=None):
        self.last_send_request = path
        success,response = Item_Base.send_request(self,path,timeout)
        return success,response

    def process_websocket_event(self, event):
        if event.control == "_3":
            if event.action == "NE": # comms error
                self.set_property ('status','alert')
                self.communication_failure()
                #self.get_status()
            elif event.action == "CE": # comms error clear
                self.set_property ('status','ready')

    def get_status(self): #isy status for node
        path = "status/" + self.address 
        success, response = self.send_request(path)     

        if success:  # and response.status == 200:
            try:
                root = ET.fromstring(response)
                node = (root.find(".//property[@id='ERR']"))

                if int(node.attrib ["value"]) == 0:
                    self.set_property ('status','ready')
                elif int(node.attrib ["value"]) > 0:
                    self.set_property ('status','alert',True)  #always publish
                    self.communications_failed()

            except Exception:
                traceback.print_exc()

        return success, response

    def communication_failure(self): # called when we receive a websocket event with a NE comm error
        log.warn("Communication Failure for {}",self.address)

    def communications_failed(self): # called when device status returns device in comm failed state
        log.warn("Communications Failed for {}",self.address)

