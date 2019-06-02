
import time

from ISY.controller import Controller

url = '192.168.1.213'

def print_events(container,item,event,*args):
    print ('Event {} from {}: {} {}'.format(event,container.container_type,item.name,args))


try:
    c = Controller(url,username='admin',password='admin',use_https=False,event_handler=print_events)
    time.sleep(2)  
    device = c.device_container.get('14 A9 92 2')
    #device = c.device_container.get('42 C8 99 1')
    print ('got device',device)

    #scene = c.scene_container.get('25770')
    #print ('got scene',scene)

    #program = c.program_container.get_program ('0022')

    var = c.variable_container.get('2:8')

    while True:
        time.sleep(2)
        #device.set_level (0)
        #device.set_speed ('low')
        #device.set_speed ('medium')
        #device.set_speed ('high')
        #scene.turn_on()
        #program.run()
        #var.set_value(1)
        time.sleep(2)
        #var.set_value(2)
        #device.set_speed ('off')
        #scene.turn_off()
        #device.set_level (100)
        #program.run_else()

except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
