# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8
 
"""

import micropython
import pyb
import gc

import util.airpy_logger as logger

from aplink.aplink_manager import APLinkManager
from attitude.attitude_controller import AttitudeController
from attitude.motor_driver import MotorDriver
from config.config_file_manager import ConfigFileManager
from util.airpy_config_utils import save_config_file, load_config_file
from receiver.rc_controller import RCController


# for better callback related error reporting
micropython.alloc_emergency_exception_buf(100)

# State Definition
IDLE = 0
ARMED = 1
FAIL_SAFE = 2

state = IDLE
updateLed = False
update_rx = False
update_attitude = False
update_motors = False
sendByte = False
newApLinkMsg = False

led = pyb.LED(4)
logger.init(logger.AIRPY_INFO)
tmpByte = bytearray(1)


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


def update_motors_state(timMotors):
    global update_motors
    update_motors = True


# for debug
def print_report():
    report = rcCtrl.get_report()
    full_report = "Valid Frames:{}  - Lost Frames:{}  - CH1:{}, CH2:{}, CH3:{}, CH4:{} - Failsafe:{}".format(
            report['Valid Frames'],
            report['Lost Frames'],
            rcCtrl.get_channel(1),
            rcCtrl.get_channel(2),
            rcCtrl.get_channel(3),
            rcCtrl.get_channel(4),
            rcCtrl.get_link_status())
    logger.info(full_report)
    # ulScheduler.add_msg(s_rep.encode('ascii'))
    # sys.stdout.write(s_rep + '    \r')


# Init Timer for status led and report
tim1 = pyb.Timer(1)
tim1.init(freq=1)
tim1.callback(status_led)

# Init Rx Timing at 300us (Frsky specific). TODO: Read RxTiming from Setting
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

# Timer for the aplink uplink mux. TODO: Read RxTiming from Setting
timApLink = pyb.Timer(4)
timApLink.init(freq=2000)
timApLink.callback(send_byte)

logger.info("AirPy v0.0.1 booting...")

# load user and application configuration files
cm = ConfigFileManager()
app_config = load_config_file("app_config.json")
rcCtrl = RCController()
attitudeCtrl = AttitudeController(cm, app_config['IMU_refresh_rate'])
attitudeCtrl.set_rc_controller(rcCtrl)
motor_driver = MotorDriver(cm, attitudeCtrl)
aplink = APLinkManager(attitudeCtrl)

# Timer for the aplink message factory
timApLinkMsg = pyb.Timer(10)
timApLinkMsg.init(freq=aplink.get_timer_freq())
timApLinkMsg.callback(send_message)

# Timer for the attitude state update
timAttitude = pyb.Timer(12)
timAttitude.init(freq=app_config['IMU_refresh_rate'])
timAttitude.callback(update_attitude_state)

# Timer for the motors state update
timMotors = pyb.Timer(13)
timMotors.init(freq=app_config['PWM_refresh_rate'])
timMotors.callback(update_motors_state)

# logger.system("Just a system test. Should create a system log")

while True:
    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False

    if updateLed:
        gc.collect()  # TODO: implement proper management of GC
        # micropython.mem_info()
        updateLed = False

    if update_attitude:
        attitudeCtrl.update_state()
        update_attitude = False

    if update_motors:
        motor_driver.set_thrust_passthrough()
        update_motors = False

    if sendByte:
        aplink.ul_scheduler.send_message()
        aplink.dl_receiver.read_byte()
        sendByte = False

    if newApLinkMsg:
        aplink.new_message()
        newApLinkMsg = False

