#! /usr/bin/env python


from ..device_lock import Device_Lock
from .device_zwave_base import Device_ZWave_Base

class Device_ZWave_Lock(Device_Lock,Device_ZWave_Base):

    def __init__(self, container, device_info):
        Device_Lock.__init__(self,container,device_info.name,device_info.address)
        Device_ZWave_Base.__init__(self,device_info)

        if device_info.properties ['ST']:
            for item in device_info.properties ['ST']:
                if item [0] == 'value':          
                    self.set_property('lock',int(item[1]))
        
        if device_info.properties ['BATLVL']:
            for item in device_info.properties ['BATLVL']:
                if item [0] == 'value':          
                    self.set_property('batterylevel',int (item[1]))

        if device_info.properties ['ERR']:
            for item in device_info.properties ['ERR']:
                if item [0] == 'value':          
                    self.set_property('error',int(item[1]))

        if device_info.properties ['USRNUM']:
            for item in device_info.properties ['USRNUM']:
                if item [0] == 'value':          
                    self.set_property('usernumber',int(item[1]))


    def process_websocket_event(self,event):

        if event.control == 'ST':
            self.set_property('lock',int(event.action))
        elif event.control == 'BATLVL':
            self.set_property('batterylevel',int(event.action))
        elif event.control == 'ERR':
            self.set_property('error',int(event.action))
        elif event.control == 'USRNUM':
            self.set_property('usernumber',int(event.action))


    def set_lock (self,mode):
        path = ('nodes/' + self.address + '/cmd/DON/' + str(mode))
        return self.send_request(path)
