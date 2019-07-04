
import time

from isy994.controller import Controller

url = '192.168.2.73'
#url = None # use autodiscovery

def print_events(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,*args))


try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=print_events)

    while True:
        time.sleep(2)


except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
