#! /usr/bin/env python

import xml.etree.ElementTree as ET

# process an event from ISY web socket client

class ISY_Event(object):

    def __init__(self,event):

        self.event = event

        node = event.find('node')
        control = event.find ('control')
        action = event.find ('action')
        event_info = event.find('eventInfo')

        self.address = node.text 
        self.control = control.text 
        self.action = action.text 
        self.event_info = event_info.text 

    def __repr__(self):
        return 'Event: Address {}, Control {}, Action {}, Event Info {}'.format(self.address,self.control,self.action,self.event_info)
    