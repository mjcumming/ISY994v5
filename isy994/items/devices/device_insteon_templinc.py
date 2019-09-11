#! /usr/bin/env python


from .device_thermostat import Device_Thermostat
from .device_insteon_base import Device_Insteon_Base

MODES = ['off','heat','cool','auto']


class Device_Insteon_TempLinc(Device_Thermostat,Device_Insteon_Base):

    def __init__(self, container, device_info):
        Device_Thermostat.__init__(self,container,device_info.name,device_info.address)
        Device_Insteon_Base.__init__(self, device_info)

        coolsetpoint_address_parts = device_info.address_parts.copy()
        coolsetpoint_address_parts [3] = '2'
        self.coolsetpoint_address = ' '.join(coolsetpoint_address_parts)

        heatsetpoint_address_parts = device_info.address_parts.copy()
        heatsetpoint_address_parts [3] = '2'
        self.heatsetpoint_address = ' '.join(heatsetpoint_address_parts)

        if device_info.properties ['ST']:
            for item in device_info.properties ['ST']:
                if item [0] == 'value':          
                    self.set_property('temperature',round(int(item[1])/2,0))
        
        if device_info.properties ['CLIMD']:
            for item in device_info.properties ['CLIMD']:
                if item [0] == 'value':          
                    self.set_property('mode',MODES [int (item[1])])

        if device_info.properties ['CLISPH']:
            for item in device_info.properties ['CLISPH']:
                if item [0] == 'value':          
                    self.set_property('heatsetpoint',round(int(item[1])/2,0))

        if device_info.properties ['CLISPC']:
            for item in device_info.properties ['CLISPC']:
                if item [0] == 'value':          
                    self.set_property('coolsetpoint',round(int(item[1])/2,0))

        if device_info.properties ['CLIHUM']:
            for item in device_info.properties ['CLIHUM']:
                if item [0] == 'value':          
                    self.set_property('humidity',round(int(item[1]),0))


    def process_websocket_event(self,event):

        if event.control == 'ST':
            self.set_property('temperature',round(int(event.action)/2,0))
        elif event.control == 'CLISPH':
            self.set_property('heatsetpoint',round(int(event.action)/2,0))
        elif event.control == 'CLISPC':
            self.set_property('coolsetpoint',round(int(event.action)/2,0))
        elif event.control == 'CLIHUM':
            self.set_property('humidity',round(int(event.action),0))
        elif event.control == 'CLIMD':
            self.set_property('mode',MODES[int(event.action)])

    def set_mode (self,mode):
        path = ('nodes/' + self.address + '/cmd/DON/' + str(mode))
        return self.send_request(path)
 
    def set_heatsetpoint (self,setpoint):
        path = ('nodes/' + self.heatsetpoint_address + '/cmd/DON/' + str(setpoint*2))
        return self.send_request(path)
 
    def set_coolsetpoint (self,setpoint):
        path = ('nodes/' + self.coolsetpoint_address + '/cmd/DON/' + str(setpoint*2))
        return self.send_request(path)
 
