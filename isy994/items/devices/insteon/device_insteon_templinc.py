#! /usr/bin/env python


from ..common.device_thermostat import Device_Thermostat
from .device_insteon_base import Device_Insteon_Base

MODES = ["None","Off", "Heat", "Cool", "Auto", "Program Auto","Program Heat","Program Cool"]
STATUS = ["Idle", "Heating", "Cooling"]

FAN_MODES = {
    0: "Off",
    7: "On",
    8: "Auto",
}


class Device_Insteon_TempLinc(Device_Thermostat, Device_Insteon_Base):
    def __init__(self, container, device_info):
        Device_Thermostat.__init__(
            self, container, device_info.name, device_info.address
        )
        Device_Insteon_Base.__init__(self, device_info)

        coolsetpoint_address_parts = device_info.address_parts.copy()
        coolsetpoint_address_parts[3] = "2"
        self.coolsetpoint_address = " ".join(coolsetpoint_address_parts)

        heatsetpoint_address_parts = device_info.address_parts.copy()
        heatsetpoint_address_parts[3] = "2"
        self.heatsetpoint_address = " ".join(heatsetpoint_address_parts)

        # print ('device properties {}'.format(device_info.properties))
        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.set_property("temperature", round(float(value) / 2, 0))
            except:
                self.set_property("temperature", 0)

        value = device_info.get_property("CLIMD", "value")
        if value:
            try:
                self.set_property("systemmode", MODES[int(value)])
            except:
                self.set_property("systemmode", 0)

        value = device_info.get_property("CLISPH", "value")
        if value:
            try:
                self.set_property("heatsetpoint", round(float(value) / 2, 0))
            except:
                self.set_property("heatsetpoint", 0)

        value = device_info.get_property("CLISPC", "value")
        if value:
            try:
                self.set_property("coolsetpoint", round(float(value) / 2, 0))
            except:
                self.set_property("coolsetpoint", 0)

        value = device_info.get_property("CLIHUM", "value")
        if value:
            try:
                self.set_property("humidity", round(float(value), 0))
            except:
                self.set_property("humidity", 0)

        value = device_info.get_property("CLIFS", "value")
        if value:
            try:
                self.set_property("fanmode", FAN_MODES[int(value)])
            except:
                self.set_property("fanmode", 0)
        value = device_info.get_property("CLIHCS", "value")
        if value:
            try:
                self.set_property("systemstatus", STATUS[int(value)])
            except:
                self.set_property("systemstatus", 0)

    def process_websocket_event(self, event):
        Device_Thermostat.process_websocket_event(self,event)

        if event.control == "ST":
            self.set_property("temperature", round(float(event.action) / 2, 0))
        elif event.control == "CLISPH":
            self.set_property("heatsetpoint", round(float(event.action) / 2, 0))
        elif event.control == "CLISPC":
            self.set_property("coolsetpoint", round(float(event.action) / 2, 0))
        elif event.control == "CLIHUM":
            self.set_property("humidity", round(float(event.action), 0))
        elif event.control == "CLIMD":
            self.set_property("systemmode", MODES[int(event.action)])
        elif event.control == "CLIFS":
            self.set_property("fanmode", FAN_MODES[int(event.action)])
        elif event.control == "CLIHCS":
            self.set_property("systemstatus", STATUS[int(event.action)])

    def set_mode(self, mode):
        path = "nodes/" + self.address + "/cmd/DON/" + str(mode)
        return self.send_request(path)

    def set_heatsetpoint(self, setpoint):
        path = "nodes/" + self.heatsetpoint_address + "/cmd/DON/" + str(setpoint * 2)
        return self.send_request(path)

    def set_coolsetpoint(self, setpoint):
        path = "nodes/" + self.coolsetpoint_address + "/cmd/DON/" + str(setpoint * 2)
        return self.send_request(path)
