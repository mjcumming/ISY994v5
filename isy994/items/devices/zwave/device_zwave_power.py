#! /usr/bin/env python


from ..device_power import Device_Power
from .device_zwave_base import Device_ZWave_Base

class Device_ZWave_Power(Device_Power,Device_ZWave_Base):

    def __init__(self, container, device_info):
        Device_Power.__init__(self,container,device_info.name,device_info.address)
        Device_ZWave_Base.__init__(self,device_info)

        value = device_info.get_property('ST','value')
        if value:
            try:
                self.set_property('power',value)
            except:
                pass

        # could capture other properties -> uofm, prec, format

    def process_websocket_event(self,event):
            if event.control == 'ST':
                self.set_property('power',event.action)