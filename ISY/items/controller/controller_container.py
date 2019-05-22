#! /usr/bin/env python

from ..item_container import Item_Container
from .controller_base import Controller_Base


import logging
logger = logging.getLogger(__name__)


class Controller_Container (Item_Container):

    def __init__(self, controller):
        Item_Container.__init__(self,controller,'Controller')

    def start(self):

        controller = Controller_Base(self,'controller')
        self.add(controller,controller.id)
         
    def controller_event(self,propery,value):
        controller = self.get('controller')
        controller.set_property(propery,value)
