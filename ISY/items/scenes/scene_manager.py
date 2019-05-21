#! /usr/bin/env python


import xml.etree.ElementTree as ET
import traceback

from .. item_manager import Item_Manager
from .scene_info import Scene_Info
from .scene_insteon import Scene_Insteon

import logging
logger = logging.getLogger(__name__)


scene_classes = {
    '6' : Scene_Insteon,
}

class Scene_Manager (Item_Manager):

    def __init__(self, controller):
        Item_Manager.__init__(self,controller,'Scene')

    def start(self):
        response = self.controller.send_request('nodes/scenes')

        try:
            if response.status_code == 200:
                root = ET.fromstring (response.content)        
                self.process_scene_nodes (root)       

                return True
            else:
                return False

        except Exception as ex:
                logger.error('scene manager Error {}'.format(ex))
                traceback.print_exc()

    def process_scene_nodes(self,root):
        for scene in root.iter('group'):
            self.process_scene_node(scene)
                
    def process_scene_node(self,node):
        scene_info = Scene_Info(node)

        if scene_info.valid: # make sure we have the info we need
            #print('process scene',scene_info)
            if scene_info.family in scene_classes:
                scene_class = scene_classes [scene_info.family]

                scene = scene_class(self,scene_info)
                self.add(scene,scene.id)
        else:
            logger.info ('invalid scene info',scene_info.name)
         
    def device_event(self,device): # notification from controller about a device event, used to "track" scene state
        for address,scene in self.scene_list.items():
            scene.device_event (device)

    def get_device(self,address):
        return self.controller.device_manager.get_device(address)
    
        

