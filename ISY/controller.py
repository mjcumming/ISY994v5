#! /usr/bin/env python

from connection import Connection
import xml.etree.ElementTree as ET


from devices.device_manager import Device_Manager 


class Controller(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):

        self._connection = Connection (address,port,username,password,use_https)

        self.device_manager = Device_Manager(self)

        self.start()

    def start(self):
        response = self.get_nodes()
        root = ET.fromstring (response.content)
        self.process_nodes(root)

    def get_nodes(self):
        response = self._connection.request('nodes')
        return response

    def process_nodes(self,root):
       
        #ET.dump(root)
        #for child in root:
            #print(child.tag, child.attrib)
        #config = root.find('deviceSpecs/model')
        #ET.dump(config)
        #model = config.find('model')
        #ET.dump(model)    	
        # 
        
        deviceList = []      
        for device in root.iter('node'):
            deviceDict = self.process_node(device)
            if deviceDict != None:
                deviceList.append(deviceDict)

    def process_node(self,node):

        self.device_manager.process_node(node)
        #ET.dump(node)
		#address = self.extractFromXML(node, 'address')
		#type = self.extractFromXML(node, 'type').split('.')
        # type is a 4-digit dotted code like 113.1.2.0.  The first # (called categoryID here) is a broad class
        # and the second number is a node type within this.  The third is version and the fourth is zero. 
        # from API manual: node category.node subcategory.version.reserved
		#categoryID = type[0]
		#subcategoryID = type[1]







url = '192.168.1.213'


if __name__ == "__main__":

    c = Controller(url,username='admin',password='admin')


