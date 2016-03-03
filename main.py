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

from aplink.aplink_manager import APLinkManager
from attitude.attitude_controller import AttitudeController
from config.config_file_manager import ConfigFileManager
from receiver.rc_controller import RCController
import util.airpy_logger as logger

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
usb = pyb.USB_VCP()
logger.init(logger.AIRPY_INFO)
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
    r = rcCtrl.get_report()
    s_rep = str('Valid Frames: ') + str(r['Valid Frames']) + str(' - Lost Frames: ') + str(r['Lost Frames'])
    s_rep += str(' - CH1: ') + str(rcCtrl.get_channel(1)) + str(', CH2: ') + str(rcCtrl.get_channel(2))
    s_rep += str(', CH3: ') + str(rcCtrl.get_channel(3)) + str(', CH4: ') + str(rcCtrl.get_channel(4))
    s_rep += str(' - Failsafe: ') + str(rcCtrl.get_link_status())
    # debug logger
    # logger.info(s_rep)
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

print("\n\rAirPy v0.0.1 booting...\n\r")

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

print("timer freq: ", aplink.get_timer_freq())

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
        attitudeCtrl.updateState()
        update_attitude = False
    if sendByte:
        tmpByte = aplink.ul_scheduler.get_message()
        if tmpByte is not None:
            usb.write(bytearray(tmpByte))  # send message to the USB
        sendByte = False
    if sendApLinkMsg:
        aplink.send_message()
        sendApLinkMsg = False
