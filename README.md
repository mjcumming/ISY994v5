# ISY994v5

Class based interface to the ISY994 device with V5 firmware.

Provides a common interface to all devices, variables, programs, and scenes on an ISY controller. 

After connecting to the ISY, the 4 types (device, scenes, programs, and variables) of items on the ISY are enumerated. The event handler generates 'add' events are items are discovered. Each item has properties that generate 'property' events as they are changed. 

Currently supports 
    Insteon dimmers, switches, keypadlincs, fanlincs, templinc and contact devices
    ZWave locks and switches
    ISY Scenes
    ISY Programs
    ISY Variables

All item/node types (device,scene,program,variable) are retrieved and updated via websockets. No polling.

Each device has a common base class so that the user does not need to aware of the technology (Insteon/zWave etc) to use that device

Designed to be easy to expand support to other ISY device types and technologies such as zWave.

Requires 5.xx firmware. Tested against 5.16. Requires chunk mode to be OFF

An event handler is supplied when the controller is started. All device events (add, remove, property) can be captured through the event handler for processing as needed.

This library is used in [IYS994-Homie-Bridge](https://pypi.org/project/ISY994-Homie3-Bridge/), an MQTT Client to serve ISY devices to a MQTT broker using the [Homie 3/4](https://homieiot.github.io/) protocol.



Example usage: The program below connects to the ISY and enumerates all items. If it finds a device with the address specified, it will flash that device on and off every 2 seconds

~~~~
import time

from isy994.controller import Controller

url = '192.168.1.213'
#url = None # use autodiscovery

dimmer_address = '42 C8 99 1' # dimmer to flash on/off

dimmer = None

def isy_event_handler(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,*args))

    if container.container_type == 'Device' and event == 'add' and item.address == dimmer_address:
        global dimmer
        dimmer = item


try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=isy_event_handler)

    while True:
        if dimmer is not None:
            dimmer.set_level (0)

        time.sleep(2)
        
        if dimmer is not None:
            dimmer.set_level (100)


except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
~~~~



