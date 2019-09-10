#! /usr/bin/env python

''' 

returns a device instance using node data from an insteon device, None if unable to create device

'''
#
# from .device_insteon_dimmer import Device_Insteon_Dimmer
# from .device_insteon_switch import Device_Insteon_Switch
# from .device_insteon_fan import Device_Insteon_Fan
# from .device_insteon_contact import Device_Insteon_Contact

from .device_zwave_controller import Device_ZWave_Controller

from .device_zwave_genericrspctl import Device_ZWave_GenericRspCtl

# insteon_device_classes = {
#     '0'  : Device_Insteon_Controller,
#     '1'  : Device_Insteon_Dimmer,
#     '2'  : Device_Insteon_Switch,
#     '14' : Device_Insteon_Switch,
#     '16' : Device_Insteon_Contact,
# }

zwave_device_classes = {
    # '118' : Device_ZWave_MultilevelSensor,
    '121' : Device_ZWave_GenericRspCtl,
    # '140' : Device_ZWave_Thermostat,
    # '143' : Device_ZWave_EnergyMonitor,
    # '155' : Device_ZWave_MotionSensor,
    # '156' : Device_ZWave_SmokeSensor,
    # '157' : Device_ZWave_TamperAlarm,
    # '172' : Device_ZWave_IntrusionAlarm,
    # '173' : Device_ZWave_TamperCodeAlarm,
    # '185' : Device_ZWave_NotificationSensor,
}

'''
dev_cat_sub_cat = {
    '1' : {
        '46' : Device_Insteon_Fan,
    },
}

'''
def get_zwave_device_class (device_info):

    #print ('Z-Wave Device Class')
    #look for specific device device cat that need special handling
    print(device_info)
    # if device_info.category == '1' and device_info.sub_category == '46' and device_info.address_parts [3] == '2': # fanlinc motor
    #     return Device_Insteon_Fan

    #print (device_info.node_def_id.find('KeypadButton') , device_info.address_parts [3])
    #override device cat for keypadlinc dimmer buttons and change to switch type devices
    # if device_info.node_def_id.find('KeypadButton') == 0 and device_info.address_parts [3] != '1': # maybe use node flag
    #     device_info.category = '2'
      
    #find device class
    #check for specific devcat/subcat

    # print (device_info, device_info.category, device_info.devtype_cat)

    if device_info.devtype_cat in zwave_device_classes:
        device_class = zwave_device_classes[device_info.devtype_cat]
        return device_class
        