#! /usr/bin/env python

import xml.etree.ElementTree as ET

from .scene_info import Scene_Info

from .scene_insteon import Scene_Insteon

scene_classes = {
    '6' : Scene_Insteon,
}

scene_events = {'add','remove','property'}

class Scene_Manager (object):

    def __init__(self, controller):
        self.controller = controller

        self.scene_list = {} # indexed by scene(node) address

    def start(self):
        response = self.controller.send_request('nodes/scenes')

        if response.status_code == 200:
            root = ET.fromstring (response.content)        
            self.process_scene_nodes (root)       

            return True
        else:
            return False
            
    def process_scene_nodes(self,root):
        for scene in root.iter('group'):
            self.process_scene_node(scene)
                
    def process_scene_node(self,node):
        scene_info = Scene_Info(node)

        if scene_info.valid: # make sure we have the info we need
            if scene_info.family in scene_classes:
                scene_class = scene_classes [scene_info.family]

                scene = scene_class(self,scene_info)
                self.add_scene(scene)
         
    def send_request(self,path,query=None): 
        return self.controller.send_request(path,query)

    def websocket_event(self,event):
        print('Scene event',event)
        scene = self.get_scene(event.address)
        scene.process_websocket_event(event)

    def add_scene(self,scene):
        self.scene_list [scene.address] = scene
        self.scene_event (scene,'add')
        print('scene',scene)

    def remove_scene(self,address):
        scene = self.scene_list [address]
        del self.scene_list [address]
        self.scene_event (scene,'remove')

    def get_scene(self,address):
        return self.scene_list [address]

    def scene_property_change(self,scene,property_,value):
        self.scene_event(scene,'property',property_,value)
    
    def scene_event(self,scene,event,*args):
        self.controller.scene_event (scene,event,args)
    
    def device_event(self,device): # notification from controller about a device event, used to "track" scene state
        for address,scene in self.scene_list.items():
            scene.device_event (device)

    def get_device(self,address):
        return self.controller.device_manager.get_device(address)
    
        

