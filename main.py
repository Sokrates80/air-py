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
from util.airpy_byte_streamer import airpy_byte_streamer

from aplink.aplink_manager import APLinkManager
from attitude.attitude_controller import AttitudeController
from config.config_file_manager import ConfigFileManager
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
sendByte = False
sendApLinkMsg = False

led = pyb.LED(4)
logger.init(logger.AIRPY_INFO)
byte_streamer = airpy_byte_streamer()
tmpByte = bytearray(1)


def send_byte(timApLink):
    global sendByte
    sendByte = True


def send_message(timApLinkMsg):
    global sendApLinkMsg
    sendApLinkMsg = True


def status_led(tim1):
    global updateLed
    updateLed = True
    led.toggle()


def update_rx_data(timRx):
    global update_rx
    update_rx = True


def updateAttitude(timAttitude):
    global update_attitude
    update_attitude = True


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
    #ulScheduler.add_msg(s_rep.encode('ascii'))
    # sys.stdout.write(s_rep + '    \r')


# Init Timer for status led and report
tim1 = pyb.Timer(1)
tim1.init(freq=1)
tim1.callback(status_led)

# Init Rx Timing at 300us (Frsky specific). TODO: Read RxTiming from Setting
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

# Timer for the aplink uplink mux
timApLink = pyb.Timer(4)
timApLink.init(freq=2000)
timApLink.callback(send_byte)

logger.info("AirPy v0.0.1 booting...")

cm = ConfigFileManager()
config = cm.configFile
rcCtrl = RCController()
attitudeCtrl = AttitudeController()
attitudeCtrl.set_rc_controller(rcCtrl)
aplink = APLinkManager(attitudeCtrl)

# Timer for the aplink message factory
timApLinkMsg = pyb.Timer(10)
timApLinkMsg.init(freq=aplink.get_timer_freq())
timApLinkMsg.callback(send_message)

# Timer for the attitude controller
timAttitude = pyb.Timer(12)
timAttitude.init(freq=20)
timAttitude.callback(updateAttitude)

logger.info("timer freq:{}".format(aplink.get_timer_freq()))
logger.system("Just a system test. Should create a system log")

while True:
    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False
    if updateLed:
        # print_report()
        gc.collect()  # TODO: implement proper management of GC
        # micropython.mem_info()
        updateLed = False
    if update_attitude:
        attitudeCtrl.update_state()
        update_attitude = False
    if sendByte:
        tmpByte = aplink.ul_scheduler.get_message()
        if tmpByte is not None:
            byte_streamer.stream_byte(tmpByte)
        sendByte = False
    if sendApLinkMsg:
        aplink.send_message()
        sendApLinkMsg = False
