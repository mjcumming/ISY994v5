#! /usr/bin/env python


from ..common.device_lock import Device_Lock
from .device_zwave_base import Device_ZWave_Base

state_map = {0: "Unlocked", 100: "Locked", 101: "Unknown", 102: "Jammed"}


class Device_ZWave_Door_Lock(Device_Lock, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Lock.__init__(self, container, device_info.name, device_info.address)
        Device_ZWave_Base.__init__(self, device_info)

        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.set_property("state", state_map.get(int(value), "Unknown"))
            except:
                pass

    def process_websocket_event(self, event):
        action = int(event.action)

        if event.control == "ST":
            self.set_property("state", state_map.get(action, "Unknown"))
        elif event.control == "ALARM":
            self.set_property("alarmcode", action)
            alarm_map = {1: "Master Code Changed", 2: "Tamper Code Entry Limit", 3: "Escutcheon Removed", 4: "Key/Manually Locked", 5: "Locked by Touch", 6: "Key/Manually Unlocked", 7: "Remote Locking Jammed Bolt", 8: "Remotely Locked", 9: "Remotely Unlocked", 10: "Deadbolt Jammed", 11: "Battery Too Low to Operate", 12: "Critical Low Battery", 13: "Low Battery", 14: "Automatically Locked", 15: "Automatic Locking Jammed Bolt", 16: "Remotely Power Cycled", 17: "Lock Handling Completed", 19: "User Deleted", 20: "User Added", 21: "Duplicate PIN", 22: "Jammed Bolt by Locking with Keypad", 23: "Locked by Keypad", 24: "Unlocked by Keypad", 25: "Keypad Attempt outside Schedule", 26: "Hardware Failure", 27: "Factory Reset"}
            self.set_property("alarm", alarm_map.get(action, "Unknown"))
        elif event.control == "BATLVL":
            self.set_property("batterylevel", action)
        elif event.control == "ERR":
            self.set_property("error", action)
        elif event.control == "USRNUM":
            self.set_property("usernumber", action)

    def lock(self):
        path = "nodes/" + self.address + "/cmd/SECMD/1"
        return self.send_request(path)

    def unlock(self):
        path = "nodes/" + self.address + "/cmd/SECMD/0"
        return self.send_request(path)
