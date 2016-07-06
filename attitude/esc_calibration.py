"""
airPy is a flight controller based on pyboard and written in micropython.

The MIT License (MIT)
Copyright (c) 2016 Fabrizio Scimia, fabrizio.scimia@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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
rcCtrl = RCController(cm)

esc_ctrl = EscController(cm, app_config['PWM_refresh_rate'])
attitudeCtrl = AttitudeController(cm, app_config['IMU_refresh_rate'], rcCtrl, esc_ctrl)

# Init Rx Timing at 300us (Frsky specific). TODO: Read RxTiming from Setting
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

while True:

    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False

    esc_ctrl.set_thrust_passthrough()
