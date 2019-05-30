#! /usr/bin/env python

''' 

returns a device instance using node data from an insteon device, None if unable to create device

'''

from .device_insteon_dimmer import Device_Insteon_Dimmer
from .device_insteon_switch import Device_Insteon_Switch
from .device_insteon_fan import Device_Insteon_Fan

insteon_device_classes = {
    '1' : Device_Insteon_Dimmer,
    '2' : Device_Insteon_Switch,
}

'''
dev_cat_sub_cat = {
    '1' : {
        '46' : Device_Insteon_Fan,
    },
}

'''
def get_insteon_device_class (device_info):

    #TBD add support for other device families
    if device_info.family == '1': #insteon devices, sanity check
        #look for specific device dev/sub cat that need special handling
        #print(device_info)
        if device_info.category == '1' and device_info.sub_category == '46' and device_info.address_parts [3] == '2': # fanlinc motor
            return Device_Insteon_Fan

        #if device_info.category in dev_cat_sub_cat and device_info.sub_category in dev_cat_sub_cat [device_info.category]:

        #override device cat for keypadlinc dimmer buttons and change to switch type devices
        if device_info.node_def_id.find('KeypadButton') and device_info.address_parts [3] != '1': # maybe use node flag
            device_info.category = '2'

        #find device class
        #check for specific devcat/subcat

        if device_info.category in insteon_device_classes:
            device_class = insteon_device_classes [device_info.category]
            return device_class
            