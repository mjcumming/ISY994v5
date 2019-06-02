#! /usr/bin/env python


from .device_contact import Device_Contact
from .device_insteon_base import Device_Insteon_Base


class Device_Insteon_Contact(Device_Contact,Device_Insteon_Base):

    def __init__(self, container, device_info):
        Device_Contact.__init__(self,container,device_info.name,device_info.address)
        Device_Insteon_Base.__init__(self, device_info)

        if device_info.property_value:
            try:
                if int(device_info.property_value) > 0:
                    self.set_property('contact','open')
                else:
                    self.set_property('contact','closed')
            except:
                pass


    def process_websocket_event(self,event):
            if event.control == 'ST':
                if int(event.action) > 0:
                    self.set_property('contact','open')
                else:
                    self.set_property('contact','closed')
