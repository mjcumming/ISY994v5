
import time

from isy994.controller import Controller

url = '192.168.1.51'
#url = None # use autodiscovery

dimmer_address = '42 C8 99 1' # dimmer to flash on/off

dimmer = None

def isy_event_handler(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,*args))

    if container.container_type == 'Device' and event == 'add' and item.address == dimmer_address:
        global dimmer
        #dimmer = item


try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=isy_event_handler)

    while True:
        if dimmer is not None:
            dimmer.set_level (0)

        time.sleep(.5)
        
        if dimmer is not None:
            dimmer.set_level (2)


except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
