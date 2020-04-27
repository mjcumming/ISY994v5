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
    # "0": Device_ZWave_Uninitialized,
    # "101": Device_ZWave_Unknown,
    # "102": Device_ZWave_Alarm,
    # "103": Device_ZWave_AV_Control_Point,
    "104": Device_ZWave_Binary_Sensor,
    # "105": Device_ZWave_Class_A_Motor_Control,
    # "106": Device_ZWave_Class_B_Motor_Control,
    # "107": Device_ZWave_Class_C_Motor_Control,
    # "108": Device_ZWave_Controller,
    # "109": Device_ZWave_Dimmer_Switch,
    # "110": Device_ZWave_Display,
    "111": Device_ZWave_Door_Lock,
    # "112": Device_ZWave_Doorbell,
    # "113": Device_ZWave_Entry_Control,
    # "114": Device_ZWave_Gateway,
    # "115": Device_ZWave_Installer_Tool,
    # "116": Device_ZWave_Motor_Multiposition,
    # "117": Device_ZWave_Climate_Sensor,
    # "118": Device_ZWave_Multilevel_Sensor,
    # "119": Device_ZWave_Multilevel_Switch,
    # "120": Device_ZWave_On_Off_Power_Strip,
    "121": Device_ZWave_On_Off_Power_Switch,
    # "122": Device_ZWave_On_Off_Scene_Switch,
    # "123": Device_ZWave_Open_Close_Valve,
    # "124": Device_ZWave_PC_Controller,
    # "125": Device_ZWave_Remote,
    # "126": Device_ZWave_Remote_Control,
    # "127": Device_ZWave_AV_Remote_Control,
    # "128": Device_ZWave_Simple_Remote_Control,
    # "129": Device_ZWave_Repeater,
    # "130": Device_ZWave_Residential_HRV,
    # "131": Device_ZWave_Satellite_Receiver,
    # "132": Device_ZWave_Satellite_Receiver,
    # "133": Device_ZWave_Scene_Controller,
    # "134": Device_ZWave_Scene_Switch,
    # "135": Device_ZWave_Security_Panel,
    # "136": Device_ZWave_Set-Top_Box,
    # "137": Device_ZWave_Siren,
    # "138": Device_ZWave_Smoke_Alarm,
    # "139": Device_ZWave_Subsystem_Controller,
    # "140": Device_ZWave_Thermostat,
    # "141": Device_ZWave_Toggle,
    # "142": Device_ZWave_Television,
    "143": Device_ZWave_Energy_Meter,
    # "144": Device_ZWave_Pulse_Meter,
    # "145": Device_ZWave_Water_Meter,
    # "146": Device_ZWave_Gas_Meter,
    # "147": Device_ZWave_Binary_Switch,
    # "148": Device_ZWave_Binary_Alarm,
    # "149": Device_ZWave_Aux_Alarm,
    # "150": Device_ZWave_CO2_Alarm,
    # "151": Device_ZWave_CO_Alarm,
    # "152": Device_ZWave_Freeze_Alarm,
    # "153": Device_ZWave_Glass_Break_Alarm,
    # "154": Device_ZWave_Heat_Alarm,
    # "155": Device_ZWave_Motion_Sensor,
    # "156": Device_ZWave_Smoke_Alarm,
    # "157": Device_ZWave_Tamper_Alarm,
    # "158": Device_ZWave_Tilt_Alarm,
    # "159": Device_ZWave_Water_Alarm,
    # "160": Device_ZWave_Door_Window_Alarm,
    # "161": Device_ZWave_Test_Alarm,
    # "162": Device_ZWave_Low_Battery_Alarm,
    # "163": Device_ZWave_CO_End_Of_Life_Alarm,
    # "164": Device_ZWave_Malfunction_Alarm,
    # "165": Device_ZWave_Heartbeat,
    # "166": Device_ZWave_Overheat_Alarm,
    # "167": Device_ZWave_Rapid_Temp_Rise_Alarm,
    # "168": Device_ZWave_Underheat_Alarm,
    # "169": Device_ZWave_Leak_Detected_Alarm,
    # "170": Device_ZWave_Level_Drop_Alarm,
    # "171": Device_ZWave_Replace_Filter_Alarm,
    # "172": Device_ZWave_Intrusion_Alarm,
    # "173": Device_ZWave_Tamper_Code_Alarm,
    # "174": Device_ZWave_Hardware_Failure_Alarm,
    # "175": Device_ZWave_Software_Failure_Alarm,
    # "176": Device_ZWave_Contact_Police_Alarm,
    # "177": Device_ZWave_Contact_Fire_Alarm,
    # "178": Device_ZWave_Contact_Medical_Alarm,
    # "179": Device_ZWave_Wakeup_Alarm,
    # "180": Device_ZWave_Timer,
    # "181": Device_ZWave_Power_Management,
    # "182": Device_ZWave_Appliance,
    # "183": Device_ZWave_Home_Health,
    "184": Device_ZWave_Barrier,
    "185": Device_ZWave_Notification_Sensor,
    # "186": Device_ZWave_Color_Switch,
    # "187": Device_ZWave_Multilevel_Switch_Off_On,
    # "188": Device_ZWave_Multilevel_Switch_Down_Up,
    # "189": Device_ZWave_Multilevel_Switch_Close_Open,
    # "190": Device_ZWave_Multilevel_Switch_Ccw_Cw,
    # "191": Device_ZWave_Multilevel_Switch_Left_Right,
    # "192": Device_ZWave_Multilevel_Switch_Reverse_Forward,
    # "193": Device_ZWave_Multilevel_Switch_Pull_Push,
    # "194": Device_ZWave_Basic_Set,
    # "195": Device_ZWave_Wall_Controller,
    # "196": Device_ZWave_Barrier_Handle,
    # "197": Device_ZWave_Sound_Switch
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
