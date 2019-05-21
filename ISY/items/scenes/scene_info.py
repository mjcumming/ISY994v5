#! /usr/bin/env python

import traceback

# process a node and assemble the info to build a scene, 
# currently only processes scenes with a flag of 132

class Scene_Info(object):

    def __init__(self,group):

        self.valid = False

        try:

            self.flag = group.attrib ['flag']
            self.id = group.attrib['nodeDefId']

            address = group.find('address')
            self.address = address.text

            name = group.find('name')
            self.name = name.text

            self.family = group.find('family').text

            if self.flag == '12': # all scene
                return 
           
            self.primary_node = group.find('pnode').text 
            
            self.device_group = group.find('deviceGroup').text

            self.controllers = [] # list of controller addresses
            self.responders = [] # list of responder addresses
            
            members = group.find('members')
            for link in members.iterfind('link'):
                link_type = link.attrib['type']
                if link_type == '0': # responder
                    self.responders.append(link.text)
                elif link_type == '16': # controller
                    self.controllers.append(link.text)

            self.valid = True

        except Exception as ex:
                print ('scene info error',ex)
                traceback.print_exc()               

    def __repr__(self):
        return 'Scene: Name {} Address {}, Family {}, Flag {}, Controllers {}, Responders {}'.format(self.name,self.address,self.family,self.flag,self.controllers,self.responders)
    