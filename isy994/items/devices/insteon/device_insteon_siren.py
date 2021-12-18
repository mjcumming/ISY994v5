#! /usr/bin/env python


from ..common.device_switch import Device_Switch
from .device_insteon_base import Device_Insteon_Base


class Device_Insteon_Siren(Device_Switch, Device_Insteon_Base):
    def __init__(self, container, device_info):
        Device_Switch.__init__(self, container, device_info.name, device_info.address)
        Device_Insteon_Base.__init__(self, device_info)

        self.add_property("duration")
        self.add_property("mode")

        value = device_info.get_property("ST", "value")
        if value:
            try:
                if int(value) > 0:
                    self.set_property("onoff", "on")
                else:
                    self.set_property("onoff", "off")
            except:
                pass

    def process_websocket_event(self, event):
        Device_Switch.process_websocket_event(self,event)

        if event.control == "ST":
            if int(event.action) > 0:
                self.set_property("onoff", "on")
            else:
                self.set_property("onoff", "off")
        elif event.control == "DUR":
            self.set_property("duration",int(event.action))
        elif event.control == "MODE":
            self.set_property("mode",int(event.action))

    def turn_on(self):
        path = "nodes/" + self.address + "/cmd/DON"
        return self.send_request(path)

    def turn_off(self):
        path = "nodes/" + self.address + "/cmd/DOF"
        return self.send_request(path)
