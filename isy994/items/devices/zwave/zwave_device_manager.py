#! /usr/bin/env python

""" 

returns a device instance using node data from an zwave device, None if unable to create device

"""

from .device_zwave_controller import Device_ZWave_Controller
from .device_zwave_door_lock import Device_ZWave_Door_Lock
from .device_zwave_on_off_power_switch import Device_ZWave_On_Off_Power_Switch
from .device_zwave_energy_meter import Device_ZWave_Energy_Meter
from .device_zwave_barrier import Device_ZWave_Barrier
from .device_zwave_binary import Device_ZWave_Binary
from .device_zwave_notification import Device_ZWave_Notification_Sensor


zwave_device_classes = {
    # '118' : Device_ZWave_MultilevelSensor,
    # '140' : Device_ZWave_Thermostat,
    # '155' : Device_ZWave_MotionSensor,
    # '156' : Device_ZWave_SmokeSensor,
    # '157' : Device_ZWave_TamperAlarm,
    # '172' : Device_ZWave_IntrusionAlarm,
    # '173' : Device_ZWave_TamperCodeAlarm,
    "104": Device_ZWave_Binary_Sensor,
    "111": Device_ZWave_Door_Lock,
    "121": Device_ZWave_On_Off_Power_Switch,
    "143": Device_ZWave_Energy_Meter,
    "184": Device_ZWave_Barrier,
    "185": Device_ZWave_Notification_Sensor,
}


def get_zwave_device_class(device_info):

    # print ('Z-Wave Device Class')
    # look for specific device device cat that need special handling
    print(device_info)
    # if device_info.category == '1' and device_info.sub_category == '46' and device_info.address_parts [3] == '2': # fanlinc motor
    #     return Device_Insteon_Fan

    # print (device_info.node_def_id.find('KeypadButton') , device_info.address_parts [3])
    # override device cat for keypadlinc dimmer buttons and change to switch type devices
    # if device_info.node_def_id.find('KeypadButton') == 0 and device_info.address_parts [3] != '1': # maybe use node flag
    #     device_info.category = '2'

    # find device class
    # check for specific devcat/subcat

    # print (device_info, device_info.category, device_info.devtype_cat)

    if device_info.devtype_cat in zwave_device_classes:
        device_class = zwave_device_classes[device_info.devtype_cat]
        return device_class
