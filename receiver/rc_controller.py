# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""
import pyb
import util.airpy_logger as logger
from receiver.sbus_receiver import SBUSReceiver


class RCController:
    def __init__(self):
        # TODO select dynamically the receiver type
        self.rcCtrl = SBUSReceiver()
        self.report = ''
        self.start_timer = 0
        self.time_count = 0
        self._IDLE = 0
        self._ARMED = 1

        logger.info("RCController Started")

    def update_rx_data(self):
        self.rcCtrl.get_new_data()

    def check_arming(self):
        check = False
        if self.get_channel(1) < 250 and self.get_channel(3) < 250 and self.get_channel(4) > 1600:
            if self.start_timer > 0:
                if pyb.elapsed_millis(self.start_timer) > 3000:  # 3 sec
                    check = True
                    self.start_timer = 0
            else:
                self.start_timer = pyb.millis()
        else:
            self.start_timer = 0

        return check

    def check_idle(self):
        check = False
        if self.get_channel(1) < 250:
            if self.start_timer > 0:
                if pyb.elapsed_millis(self.start_timer) > 5000:  # 5 sec
                    check = True
                    self.start_timer = 0
            else:
                self.start_timer = pyb.millis()
        else:
            self.start_timer = 0

        return check

    def get_report(self):
        self.report = self.rcCtrl.get_rx_report()
        return self.report

    def get_channels(self):
        return self.rcCtrl.get_rx_channels()

    def get_channel(self, num_channel):
        return self.rcCtrl.get_rx_channel(num_channel - 1)  # convert from 0->n to 1->(n+1)

    def get_link_status(self):
        return self.rcCtrl.get_failsafe_status()
