#! /usr/bin/env python


from ..common.device_dimmer import Device_Dimmer
from .device_insteon_base import Device_Insteon_Base

paddle_events = {"DON", "DON3", "DON4", "DON5", "DOF", "DOF3", "DOF4", "DOF5", "DIM", "BRT", "DFON", "DFOF", "FDUP", "FDDOWN", "FDSTOP"}


class Device_Insteon_Dimmer(Device_Dimmer, Device_Insteon_Base):
    def __init__(self, container, device_info):
        Device_Dimmer.__init__(self, container, device_info.name, device_info.address)
        Device_Insteon_Base.__init__(self, device_info)
        # print(device_info)

        self.add_property("paddle_action")

        value = device_info.get_property("ST", "value")
        if value:
            try:
                self.properties["level"] = int(int(value) / 255 * 100)
            except:
                pass

    def process_websocket_event(self, event):
        Device_Dimmer.process_websocket_event(self,event)

        if event.control == "ST":
            self.set_property("level", int(int(event.action) / 255 * 100))
            # print ('device {}. changed status to {}'.format(self.name,event.action))

        elif event.control in paddle_events:  # need to add other events
            self.set_property("paddle_action", event.control, True)
            # print ('device {}. changed local control {}'.format(self.name,event.action))

    def set_level(self, level):
        path = "nodes/" + self.address + "/cmd/DON/" + str(int(level / 100 * 255))
        return self.send_request(path)

    # def fade_up(self):
    #    path = "nodes/" + self.address + "/cmd/FDUP/startlevel/" + str(int(level / 100 * 255))
    #    return self.send_request(path)

    # def fade_down(self):
    #    path = "nodes/" + self.address + "/cmd/FDDOWN/startlevel/" + str(int(level / 100 * 255))
    #    return self.send_request(path)

    def fade_stop(self):
        path = "nodes/" + self.address + "/cmd/FDSTOP"
        return self.send_request(path)

    def fast_on(self):
        path = "nodes/" + self.address + "/cmd/DFON"
        return self.send_request(path)

    def fast_off(self):
        path = "nodes/" + self.address + "/cmd/DFOF"
        return self.send_request(path)

    def brighten(self):
        path = "nodes/" + self.address + "/cmd/BRT"
        return self.send_request(path)

    def dim(self):
        path = "nodes/" + self.address + "/cmd/DIM"
        return self.send_request(path)
