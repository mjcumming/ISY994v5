#! /usr/bin/env python


# process a node and assemble the info to build a program


class Program_Info(object):
    def __init__(self, node):

        self.node = node

        self.valid = False

        try:
            self.id = node.attrib["id"]
            self.name = node.find("name").text
            self.folder = node.attrib["folder"] == "true"  # program folder, not interested

            if self.folder is False:
                self.enabled = node.attrib["enabled"] == "true"
                self.last_run_time = node.find("lastRunTime").text
                self.last_finish_time = node.find("lastFinishTime").text

            self.valid = True

        except Exception as err:
            self.err = err

    def __repr__(self):
        if self.valid is True:
            return "Program: Name {} ID {}".format(self.name, self.id)
        else:
            return "Invalid program node: {}".format(self.err)

