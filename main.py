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

# import micropython
import pyb
import gc
import utils.airpy_logger as logger
from aplink.aplink_manager import APLinkManager
from attitude.attitude_controller import AttitudeController
from attitude.esc_controller import EscController
from config.config_file_manager import ConfigFileManager
from utils.airpy_config_utils import load_config_file
from receiver.rc_controller import RCController


# for better callback related error reporting
# micropython.alloc_emergency_exception_buf(100)

# State Definition
IDLE = 0
ARMED = 1
FAIL_SAFE = 2

# set initial state as IDLE
state = IDLE

updateLed = False
update_rx = False
update_attitude = False
update_motors = False
sendByte = False
newApLinkMsg = False

led = pyb.LED(4)
led_armed = pyb.LED(1)
logger.init(logger.AIRPY_INFO)


def send_byte(timApLink):
    global sendByte
    sendByte = True


def send_message(timApLinkMsg):
    global newApLinkMsg
    newApLinkMsg = True


def status_led(tim1):
    global updateLed
    updateLed = True
    led.toggle()


def update_rx_data(timRx):
    global update_rx
    update_rx = True


def update_attitude_state(timAttitude):
    global update_attitude
    update_attitude = True


def set_state(new_state):
    global state
    global led_armed
    if new_state == ARMED:
        state = ARMED
        led_armed.on()
    if new_state == IDLE:
        state = IDLE
        led_armed.off()

logger.info("AirPy v0.0.1 booting...")

# load user and application configuration files

cm = ConfigFileManager()
app_config = load_config_file("app_config.json")
aplink_active = app_config['aplink_enabled']
rcCtrl = RCController(cm)
esc_ctrl = EscController(cm, app_config['PWM_refresh_rate'])
attitudeCtrl = AttitudeController(cm, app_config['IMU_refresh_rate'], rcCtrl, esc_ctrl)

# Free some memory
cm = None
gc.collect()

# Init Timer for status led (1 sec interval)
tim1 = pyb.Timer(1)
tim1.init(freq=1)
tim1.callback(status_led)

# Init Rx Timing at 300us (Frsky specific). TODO: Read Rx freq from rc_ctrl
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

# Timer for the attitude state update
timAttitude = pyb.Timer(12)
timAttitude.init(freq=app_config['IMU_refresh_rate'])
timAttitude.callback(update_attitude_state)

# Free some memory
app_config = None
gc.collect()

if aplink_active:
    aplink = APLinkManager(attitudeCtrl)

    # Timer for the aplink uplink mux. TODO: Read freq from Setting
    timApLink = pyb.Timer(4)
    timApLink.init(freq=aplink.get_timer_freq()*10)
    timApLink.callback(send_byte)

    # Timer for the aplink message factory
    timApLinkMsg = pyb.Timer(10)
    timApLinkMsg.init(freq=aplink.get_timer_freq())
    timApLinkMsg.callback(send_message)

while True:

    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False

    if updateLed:
        gc.collect()  # TODO: implement proper management of GC
        # micropython.mem_info()

        if state == IDLE:
            if rcCtrl.check_arming():
                set_state(ARMED)
                logger.info("Set status to ARMED")
        elif state == ARMED:
            if rcCtrl.check_idle():
                set_state(IDLE)
                logger.info("Set status to IDLE")
        updateLed = False

    if update_attitude:
        attitudeCtrl.update_state()
        attitudeCtrl.update_esc(state)
        update_attitude = False

    if sendByte:
        aplink.ul_scheduler.send_message()
        aplink.dl_receiver.read_byte()
        sendByte = False

    if newApLinkMsg:
        aplink.new_message()
        newApLinkMsg = False


