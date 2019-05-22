#! /usr/bin/env python

''' 

Base Program

<eventInfo>
    <id>1C</id>
    <on />
    <nr />
    <r>190520 08:28:16</r>
    <f>190520 08:28:16</f>
    <s>31</s>
</eventInfo>

'''
from .. item_base import Item_Base

class Program_Base(Item_Base):

    def __init__(self, container, program_info):
        Item_Base.__init__(self,container)

        self.add_property('state', 'idle') #program run state

        self.id = program_info.id
        self.name = program_info.name
        self.add_property('last_run_time', program_info.last_run_time)
        self.add_property('last_finish_time', program_info.last_finish_time)

    def __str__(self):
        return ("Program: {}; id {}; run {}, finish {}".format(self.name, self.id, self.properties['last_run_time'], self.properties['last_finish_time']))

    def process_websocket_event(self,state_code,last_run_time,last_finish_time):
        state = 'unknown'
        if state_code & 1 == 1:
            state = 'idle'
        elif state_code & 2 == 2:
            state = 'then'
        elif state_code & 3 == 3:
            state = 'else'

        self.set_property('state',state)
        self.set_property('last_run_time',last_run_time)
        self.set_property('last_finish_time',last_finish_time)

    def command(self,command):
        path = 'programs/' + self.id + '/' + command
        return self.send_request(path)        

    def run(self):
        self.command('run')

    def stop(self):
        self.command('stop')

    def run_then(self):
        self.command('runThen')

    def run_else(self):
        self.command('runElse')

    def enable(self):
        self.command('enable')

    def disable(self):
        self.command('disable')
        
        
        