#! /usr/bin/env python

import time
import traceback
import threading
from datetime import datetime
from datetime import timedelta
import asyncio 

from .items.devices.device_container import Device_Container
from .items.scenes.scene_container import Scene_Container
from .items.variables.variable_container import Variable_Container
from .items.programs.program_container import Program_Container
from .items.controller.controller_container import Controller_Container

from .network.discover import Discover
from .network.async_session import Async_Session

from .support.repeating_timer import Repeating_Timer

import logging

logger = logging.getLogger(__name__)

# event categores controller, device, scene, variable, program


class Controller(object):
    def __init__(
        self,
        address=None,
        port=80,
        username="admin",
        password="admin",
        use_https=False,
        event_handler=None,
    ):
        if address == None:
            discover = Discover()
            controller_list = discover.start()
            if len(controller_list) > 0:
                address = controller_list[0]

        if address is None:
            logger.error("No controller address found")
            quit()

        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.use_https = use_https

        self.event_handler = event_handler

        self.controller_container = Controller_Container(self)
        self.device_container = Device_Container(self)
        self.scene_container = Scene_Container(self)
        self.variable_container = Variable_Container(self)
        self.program_container = Program_Container(self)

        self.last_heartbeat = datetime.now()
        self.heartbeat_interval = 30  # set below by data from controller, needed here for watchdog if no initial connection

        self.controller_container.start()

        self.connect()
        self.start()

        self.watch_dog_timer = Repeating_Timer(
            30
        )  # left over from websocket client - may remove as it does nothing
        self.watch_dog_timer.add_callback(self.watch_dog_check)

    def connect(self):
        def start():
            try:
                asyncio.set_event_loop(self.event_loop)
                self.event_loop.run_forever()
                logger.warning ('Event loop stopped')
                #self.session.close()
            except:
                logger.error ('Error in event loop')

        self.event_loop = asyncio.new_event_loop()

        self.session = Async_Session(
            self,
            self.address,
            self.port,
            self.username,
            self.password,
            False,
            loop=self.event_loop,
        )

        logger.warning("Starting Session thread")
        self._ws_thread = threading.Thread(target=start, args=())

        self._ws_thread.daemon = True
        self._ws_thread.start()

    def start(self):
        self.process_controller_event("status", "init")

        if self.get_controller_items() is True:
            self.process_controller_event("status", "ready")
            self.connect_websocket()
        else:
            self.process_controller_event("status", "error")
            self.retry_start(10)

    def retry_start(self, delay_seconds):
        def restart():
            self.start()

        self.restart_timer = threading.Timer(delay_seconds, restart)
        self.restart_timer.start()

    def get_controller_items(self):
        success = True

        if self.device_container.items_retrieved is False:
            if self.device_container.start() is False:
                success = False

        if self.scene_container.items_retrieved is False:
            if self.scene_container.start() is False:
                success = False

        if self.variable_container.items_retrieved is False:
            if self.variable_container.start() is False:
                success = False

        if self.program_container.items_retrieved is False:
            if self.program_container.start() is False:
                success = False

        succ, _ = self.controller_container.get_controller_time()
        if succ is False:
            success = False

        return success

    def connect_websocket(self):
        self.session.start_websocket()

    def container_event(self, container, item, event, *args):
        logger.debug(
            "Container Event {} from .{}: {} {}".format(
                item.name, container.container_type, item, args
            )
        )
        self.publish_container_event(container, item, event, *args)

        if (
            container.container_type == "Device"
        ):  # propagate to scene container to see if we should update scene states
            self.scene_container.device_event(item)

    def publish_container_event(self, container, item, event, *args):
        try:
            self.event_handler(container, item, event, *args)
        except Exception as ex:
            logger.error("Event handler Error {}".format(ex))
            traceback.print_exc()

    def send_request(self, path, timeout=None):
        success, response = self.session.request(path, timeout)
        return success, response

    def http_connected(self, connected):  # True HTTP connected, False, no connection
        if connected:
            self.process_controller_event("http", "connected")
        else:
            self.process_controller_event("http", "disconnected")

    def websocket_connected(
        self, connected
    ):  # True websocket connected, False, no connection
        if connected:
            self.process_controller_event("websocket", "connected")
        else:
            self.process_controller_event("websocket", "disconnected")

    def websocket_event(self, event):  # process websocket event
        logger.info("Websocket Event {}".format(event))

        try:
            if event.address is not None:  # event from .a device/node
                self.device_container.websocket_event(event)

            if event.control == "_0":  # heartbeat
                self.process_heartbeat(event)

            elif event.control == "_1":  # trigger
                if event.action == "0":  # program
                    self.program_container.websocket_event(event)
                elif event.action == "6":  # variable change
                    self.variable_container.websocket_event(event)

            elif event.control == "_5":  # system status
                self.process_system_status(event)

        except Exception as ex:
            logger.error("websocket handler Error {}".format(ex))
            traceback.print_exc()

    def process_controller_event(self, property_, value):
        controller = self.controller_container.get("controller")
        controller.set_property(property_, value)

    def process_heartbeat(self, event):
        self.last_heartbeat = datetime.now()  # .strftime("%m/%d/%Y, %H:%M:%S")
        self.process_controller_event("heartbeat", self.last_heartbeat)
        self.heartbeat_interval = int(event.action)

    def process_system_status(self, event):
        if event.action == "0":  # idle
            self.process_controller_event("state", "idle")
        elif event.action == "1":  # busy
            self.process_controller_event("state", "busy")

    def watch_dog_check(self):
        if (
            self.last_heartbeat + timedelta(seconds=self.heartbeat_interval)
            < datetime.now()
        ):
            logger.warning("Watchdog timer triggered.")

    def close(self):
        self.event_loop.stop()
        self._ws_thread.join()
        self.session.close()