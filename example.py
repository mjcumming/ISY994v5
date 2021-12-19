
import time

from isy994.controller import Controller

url = '192.168.1.51'
#url = None # use autodiscovery

dimmer_address = '42 C8 99 1' # dimmer to flash on/off
switch_address = '0 5A B8 1' # switch to flash on/off

dimmer_address = '0 5A B8 1' # switch to flash on/off

dimmer = None
switch = None

def isy_event_handler(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,*args))

    if container.container_type == 'Device' and event == 'add' and item.address == dimmer_address:
        global dimmer
        dimmer = item

    if container.container_type == 'Device' and event == 'add' and item.address == switch_address:
        global switch
        #switch = item

c = None

try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=isy_event_handler)

    while True:
        if dimmer is not None:
            success, response = dimmer.set_level (0)
            print ("dimmer {} ----------  {}".format(success, response))

        if switch is not None:
            print ("switch {} {}".format(switch.turn_off()))

        time.sleep(2)
        
        if dimmer is not None:
            dimmer.set_level (20)
            dimmer.get_status()

        if switch is not None:
            switch.turn_on()
            switch.get_status()

        time.sleep(2)


except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
    c.close()
    print ('Closed session')

finally:
    print ('Done')