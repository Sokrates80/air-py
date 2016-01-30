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

from aplink.aplink_manager import APLinkManager
from attitude.attitude_controller import AttitudeController
from config.config_file_manager import ConfigFileManager
from receiver.rc_controller import RCController
import util.airpy_logger as logger

# for better callback related error reporting
micropython.alloc_emergency_exception_buf(100)

updateLed = False
update_rx = False
sendApLinkMux = False
sendApLinkMsg = False

led = pyb.LED(4)
logger.init(logger.AIRPY_INFO)


def send_byte(timApLink_mux):
    global sendApLinkMux
    sendApLinkMux = True


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
timApLink.init(freq=100)
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

print("timer freq: ", aplink.get_timer_freq())

while True:
    if update_rx:
        rcCtrl.update_rx_data()
        update_rx = False
    if updateLed:
        # print_report()
        updateLed = False
    if sendApLinkMux:
        tmpByte = aplink.ul_mux.read_queue()
        if tmpByte is not None:
            print(chr(tmpByte))
        sendApLinkMux = False
    if sendApLinkMsg:
        aplink.send_message()
        sendApLinkMsg = False
