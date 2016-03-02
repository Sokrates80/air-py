# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""
import util.airpy_logger as logger


class AttitudeController:
    def __init__(self):
        self.rc_control = None
        logger.info("AttitudeController Started")

    def set_rc_controller(self, rcCtrl):
        self.rc_control = rcCtrl

    def get_rc_controller(self):
        return self.rc_control
