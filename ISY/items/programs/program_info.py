#! /usr/bin/env python


# process a node and assemble the info to build a program


class Program_Info(object):

    def __init__(self,node):

        self.node = node

        self.valid = False

        try:
            if node.attrib ['folder'] == 'true': # program folder, not interested
                return

            if node.attrib ['enabled'] == 'false': # not enabled
                return

            self.id = node.attrib ['id']
            self.name = node.find('name').text
            self.last_run_time = node.find('lastRunTime').text
            self.last_finish_time = node.find('lastFinishTime').text

            self.valid = True
        except:
            pass

    def __repr__(self):
        return 'Program: Name {} ID {}'.format(self.name,self.id)
    