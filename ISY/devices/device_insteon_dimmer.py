#! /usr/bin/env python


#Device: Kids Bathroom Vanity Light ; address 50 A 83 1 ; cat 1, sub_cat 32, version 69, parent 27840
#<node flag="128" nodeDefId="DimmerLampSwitch_ADV"><address>50 A 83 1</address><name>Kids Bathroom Vanity Light</name><parent type="3">27840</parent><type>1.32.69.0</type><enabled>true</enabled><deviceClass>0</deviceClass><wattage>0</wattage><dcPeriod>0</dcPeriod><startDelay>0</startDelay><endDelay>0</endDelay><pnode>50 A 83 1</pnode><property formatted="100%" id="ST" uom="100" value="255" /></node>

from .device_base import Device_Base

paddle_events = {'DON','DOFF','DIM','BRT','DFON','DFOF'}

class Device_Insteon_Dimmer(Device_Base):

    def __init__(self, parent, device_info):
        Device_Base.__init__(self,parent, device_info)

        self.add_property('level',0) #in percent
        self.add_property('paddle_action')
        
        
        if device_info.property_value:        
            try:
                self.level = int(int(device_info.property_value)/255*100)
            except:
                pass

    def process_websocket_event(self,event):
            #print ('device event')
            if event.control == 'ST':
                self.set_property('level',int(event.action)/255*100)
                #print ('device {}. changed status to {}'.format(self.name,event.action))

            elif event.control in paddle_events: #need to add other events
                self.set_property('paddle_action',event.control)
                #print ('device {}. changed local control {}'.format(self.name,event.action))

    def set_level(self,level):
        path = ('nodes/' + self.address + '/cmd/DON/' + str(int(level*255)))
        return self.send_request(path)

    def fast_on(self):
        path = ('nodes/' + self.address + '/cmd/DFON')
        return self.send_request(path)

    def fast_off(self):
        path = ('nodes/' + self.address + '/cmd/DFOF')
        return self.send_request(path)

    def brighten(self):
        path = ('nodes/' + self.address + '/cmd/BRT')
        return self.send_request(path)

    def dim(self):
        path = ('nodes/' + self.address + '/cmd/DIM')
        return self.send_request(path)
