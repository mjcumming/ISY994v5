#! /usr/bin/env python


import xml.etree.ElementTree as ET

class ISY_Event(object):

    def __init__(self,message):

        event = ET.fromstring (message)
        self.event = event
        
        node = event.find('node')
        control = event.find ('control')
        action = event.find ('action')
        event_info = event.find('eventInfo')

        self.node = node.text 
        self.control = control.text 
        self.action = action.text 
        self.event_info = event_info.text 

    def __repr__(self):
        return 'Event: Control {}, Action {}, Node {}, Event Info {}'.format(self.control,self.action,self.node,self.event_info)
    