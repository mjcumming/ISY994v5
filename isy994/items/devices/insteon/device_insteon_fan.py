#! /usr/bin/env python


from ..device_fan import Device_Fan
from .device_insteon_base import Device_Insteon_Base

speeds=['off','low','medium','high']

class Device_Insteon_Fan(Device_Fan,Device_Insteon_Base):

    def __init__(self, container, device_info):
        Device_Fan.__init__(self,container,device_info.name,device_info.address,speeds)
        Device_Insteon_Base.__init__(self,device_info)

        if device_info.property_value:
            self.set_property ('speed',self.level_to_speed(int(device_info.property_value)))

    def process_websocket_event(self,event):
            if event.control == 'ST':
                self.set_property ('speed',self.level_to_speed(int(event.action)))

    def set_speed (self,speed):
        level = self.speed_to_level(speed)
        path = ('nodes/' + self.address + '/cmd/DON/' + str(level))
        return self.send_request(path)
 
    def level_to_speed(self,level):
        if level == 0:
            return'off'
        elif level > 0 and level <= 63:
            return 'low'
        elif level >= 50 and level <= 191:
           return 'medium'
        else:
            return 'high'

    def speed_to_level(self,speed):
        if speed == 'off':
            return 0
        elif speed == 'low':
            return 63
        elif speed == 'medium':
            return 99
        else:
            return 255



