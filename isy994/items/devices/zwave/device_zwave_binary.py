#! /usr/bin/env python


from ..common.device_binary import Device_Binary
from .device_zwave_base import Device_ZWave_Base


class Device_ZWave_Binary(Device_Binary, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Binary.__init__(self, container, device_info.name, device_info.address)
        Device_ZWave_Base.__init__(self, device_info)

        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.set_property("binary", value)
            except:
                pass

    def process_websocket_event(self, event):
        if event.control == "ST":
            if event.action:
                self.set_property("binary", event.action)
