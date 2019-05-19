#! /usr/bin/env python


from .variable_base import Variable_Base

class Variable_State(Variable_Base):

    def __init__(self, parent, variable_info):
        Variable_Base.__init__(self,parent, variable_info)
