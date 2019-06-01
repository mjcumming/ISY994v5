#! /usr/bin/env python


from .device_switch import Device_Switch
from .device_insteon_base import Device_Insteon_Base

paddle_events = {'DON','DOFF','DIM','BRT','DFON','DFOF'}

class Device_Insteon_Switch(Device_Switch,Device_Insteon_Base):

    def __init__(self, container, device_info):
        Device_Switch.__init__(self,container,device_info.name,device_info.address)
        Device_Insteon_Base.__init__(self,device_info)

        self.add_property('paddle_action')

        if device_info.property_value:
            try:
                if int(device_info.property_value) > 0:
                    self.set_property('onoff','on')
                else:
                    self.set_property('onoff','off')
            except:
                pass

    def process_websocket_event(self,event):
            if event.control == 'ST':
                if int(event.action) > 0:
                    self.set_property('onoff','on')
                else:
                    self.set_property('onoff','off')

            elif event.control in paddle_events: #need to add other events
                self.set_property('paddle_action',event.control)

    def turn_on(self):
        path = ('nodes/' + self.address + '/cmd/DON')
        return self.send_request(path)

    def turn_off(self):
        path = ('nodes/' + self.address + '/cmd/DOF')
        return self.send_request(path)
