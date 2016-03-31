# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Thu Apr 01 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

01-Apr-2016 Initial Release

"""

import pyb
from attitude.attitude_controller import AttitudeController
from attitude.esc_controller import EscController
from config.config_file_manager import ConfigFileManager
from util.airpy_config_utils import load_config_file
from receiver.rc_controller import RCController

pyb.LED(1).on()  # red led indicting motor armed
update_rx = False
update_attitude = False


def update_rx_data(timRx):
    global update_rx
    update_rx = True


def update_attitude_state(timAttitude):
    global update_attitude
    update_attitude = True

print("Esc Calibration Mode")

# load user and application configuration files
cm = ConfigFileManager()
app_config = load_config_file("app_config.json")
rcCtrl = RCController()
attitudeCtrl = AttitudeController(cm, app_config['IMU_refresh_rate'])
attitudeCtrl.set_rc_controller(rcCtrl)
esc_ctrl = EscController(cm, attitudeCtrl, app_config['PWM_refresh_rate'])


# Init Rx Timing at 300us (Frsky specific). TODO: Read RxTiming from Setting
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

# Timer for the attitude state update
timAttitude = pyb.Timer(12)
timAttitude.init(freq=app_config['IMU_refresh_rate'])
timAttitude.callback(update_attitude_state)

while True:

    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False

    if update_attitude:
        esc_ctrl.set_thrust_passthrough()
        update_attitude = False