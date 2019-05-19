#! /usr/bin/env python

import xml.etree.ElementTree as ET

class Variable_Info(object):

    def __init__(self,node):

        self.valid = False

        try:

            self.id = node.attrib['id']
            self.type = node.attrib['type']
            self.init_value = int(node.find('init').text)
            self.value = int(node.find('val').text)
            self.time_set = node.find('ts').text

            self.valid = True

        except:
            pass

    def __repr__(self):
        return 'Variable: ID {} Value {}, Init {}, Time {}'.format(self.id,self.value,self.init,self.time_set)
    