# ISY994v5

Class based interface to the ISY994 device with V5 firmware.

Provides a common interface to all devices, variables, programs, and scenes on an ISY controller. 

Currently supports Insteon dimmers, switches, keypadlincs, fanlincs, and contact devices. 

Designed to be easy to expand support to other device types and technologies such as zWave.

Requires 5.xx firmware. Tested against 5.12

An event handler is supplied when the controller is started. All device events (add, remove, property) can be captured through the event handler for processing as needed.

This library is used in [IYS994-Homie-Bridge](https://pypi.org/project/ISY994-Homie3-Bridge/), an MQTT Client to serve ISY devices to a MQTT broker using the [Homie 3](https://homieiot.github.io/) protocol.

Example usage: 

~~~~
import time

from isy.controller import Controller

url = 'xxx.xxx.xxx.xxx'
#url = None # use autodiscovery

def print_events(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,*args))

try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=print_events)

    while True:
        time.sleep(2)

except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
~~~~

This package requires further development and testing.


