# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""
from receiver.sbus_receiver import SBUSReceiver


class RCController:
    def __init__(self):
        # TODO select dynamically the receiver type
        self.rcCtrl = SBUSReceiver()
        self.report = ''
        print("RCController Started")

    def update_rx_data(self):
        self.rcCtrl.get_new_data()

    def get_report(self):
        self.report = self.rcCtrl.get_rx_report()
        return self.report

    def get_channels(self):
        return self.rcCtrl.get_rx_channels()

    def get_channel(self, num_channel):
        return self.rcCtrl.get_rx_channel(num_channel - 1)  # convert from 0->n to 1->(n+1)

    def get_link_status(self):
        return self.rcCtrl.get_failsafe_status()
