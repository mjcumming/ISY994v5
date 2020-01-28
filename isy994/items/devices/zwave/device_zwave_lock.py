#! /usr/bin/env python


from ..common.device_lock import Device_Lock
from .device_zwave_base import Device_ZWave_Base


class Device_ZWave_Lock(Device_Lock, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Lock.__init__(self, container, device_info.name, device_info.address)
        Device_ZWave_Base.__init__(self, device_info)

        value = device_info.get_property("ST", "value")
        if value:
            try:
                if int(value) > 0:
                    self.set_property("state", "Locked")
                else:
                    self.set_property("state", "Unlocked")
            except:
                pass

    def process_websocket_event(self, event):

        if event.control == "ST":
            state_map = {0: "Unlocked", 100: "Locked"}
            self.set_property("state", state_map[int(event.action)])
        elif event.control == "BATLVL":
            self.set_property("batterylevel", int(event.action))
        elif event.control == "ERR":
            self.set_property("error", int(event.action))
        elif event.control == "USRNUM":
            self.set_property("usernumber", int(event.action))

    def lock(self):
        path = "nodes/" + self.address + "/cmd/SECMD/1"
        return self.send_request(path)

    def unlock(self):
        path = "nodes/" + self.address + "/cmd/SECMD/0"
        return self.send_request(path)
