#! /usr/bin/env python

""" 
Only contains the ISY controller item, use the container for consistency
"""
from ..item_base import Item_Base


class Controller_Base(Item_Base):
    def __init__(self, container, id):
        Item_Base.__init__(self, container, "ISY Controller")

        self.id = id
        self.name = id

        self.add_property("state", "idle")
        self.add_property("heartbeat", "none")
        self.add_property("websocket", "disconnnected")
        self.add_property("http", "disconnected")

    def __str__(self):
        return "Controller: {}; state {}; status {}".format(
            self.id, self.properties["state"], self.properties["status"]
        )

    def get_identifier(self):
        return self.id

    def get_controller_time(self):
        success, response = self.send_request("time")
        if success:
            pass
        return success, response
