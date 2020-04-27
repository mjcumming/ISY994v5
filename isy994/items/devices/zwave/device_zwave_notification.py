#! /usr/bin/env python


from ..common.device_notification import Device_Notification
from .device_zwave_base import Device_ZWave_Base


class Device_ZWave_Notification(Device_Notification, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Notification.__init__(self, container, device_info.name, device_info.address)
        Device_ZWave_Base.__init__(self, device_info)

        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.set_property("notification", value)
            except:
                pass

    def process_websocket_event(self, event):
        if event.control == "ST":
            self.set_property("notification", event.action)
        elif event.control == "BATLVL":
            self.set_property("batterylevel", int(event.action))
