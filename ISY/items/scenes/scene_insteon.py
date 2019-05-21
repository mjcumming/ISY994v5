#! /usr/bin/env python


from .scene_base import Scene_Base

class Scene_Insteon(Scene_Base):

    def __init__(self, container, scene_info):
        Scene_Base.__init__(self,container, scene_info)

        self.add_property('state')

    def process_websocket_event(self,event):
        pass # there are no events for scenes AFAICT

    def turn_on(self):
        path = ('nodes/' + self.address + '/cmd/DON')
        return self.send_request(path)

    def turn_off(self):
        path = ('nodes/' + self.address + '/cmd/DOF')
        return self.send_request(path)

    def device_event(self,device): #device event, process and see if we are interested
        if device.family == '1': #insteon device
            if device.address in self.responders: # this scene has this device
                scene_state = 'off'
                for address in self.responders:
                    device = self.container.get_device(address)
                    if device is not None:
                        if device.category == '1': #insteon dimmer
                            if device.get_property ('level') > 0:
                                scene_state ='on'
                        if device.category == '2': #insteon switch
                            if device.get_property ('onoff') == 'on':
                                scene_state ='on'
                
                if scene_state != self.properties ['state']:
                    self.set_property ('state',scene_state)

