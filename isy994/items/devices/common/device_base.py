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
        
        if Item_Base.get_property("status") == "alert": # request an update when sending a command in an alert state
            self.get_status()

        return success,response

    def process_websocket_event(self, event):
        if event.control == "_3":
            if event.action == "NE": # comms error
                self.set_property ('status','alert')
            elif event.action == "CE": # comms error clear
                self.set_property ('status','ready')

            #print ("*****ERRROR STATE {} {}".format(self.name,self.get_property("status")))       

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

            except Exception:
                traceback.print_exc()

        return success, response