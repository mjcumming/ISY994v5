#! /usr/bin/env python


from ..common.device_base import Device_Base
from .device_zwave_base import Device_ZWave_Base

paddle_events = {"DON", "DOF", "DIM", "BRT", "DFON", "DFOF"}


class Device_ZWave_Controller(Device_Base, Device_ZWave_Base):
    def __init__(self, container, device_info):
        Device_Base.__init__(
            self, container, "controller", device_info.name, device_info.address
        )
        Device_ZWave_Base.__init__(self, device_info)

        self.add_property("paddle_action")

    def process_websocket_event(self, event):
        if event.control in paddle_events:
            self.set_property("paddle_action", event.control, True)

