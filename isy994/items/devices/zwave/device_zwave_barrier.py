#! /usr/bin/env python


from ..common.device_barrier import Device_Barrier
from .device_zwave_base import Device_ZWave_Base

state_map = {0: "closed", 100: "open", 101: "unknown", 102: "stopped", 103: "closing", 104: "opening"}


class Device_ZWave_Barrier(Device_Barrier, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Barrier.__init__(self, container, device_info.name, device_info.address)
        Device_ZWave_Base.__init__(self, device_info)

        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.set_property("barrier", int(value)))
                if (int(value) > 0 and int(value) < 100):
                    self.set_property("state", "percent closed")
                else:
                    self.set_property("state", state_map.get(int(value), "unknown"))
            except:
                pass

    def process_websocket_event(self, event):
        action = int(event.action)

        if event.control == "ST":
            self.set_property("barrier", action))
            if (action > 0 and action < 100):
                self.set_property("state", "percent closed")
            else:
                self.set_property("state", state_map.get(action, "unknown"))
