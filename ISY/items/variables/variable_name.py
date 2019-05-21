#! /usr/bin/env python

import xml.etree.ElementTree as ET


class Variable_Name(object):

    def __init__(self,node):

        self.valid = False

        try:

            self.id = node.attrib['id']
            self.name = node.attrib['name']
            self.value = int(node.find('val').text)
            self.valid = True

        except:
            pass

    def __repr__(self):
        return 'Variable: ID {} Name {}, Value {}'.format(self.id,self.name,self.value)
    