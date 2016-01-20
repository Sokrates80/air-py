# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:29:48 2015

@author: fabrizioscimia
"""

class AttitudeController:
    def __init__(self):
        print("AttitudeController Started")

    def setRcController(self, rcCtrl):
        self.rcControl = rcCtrl

    def getRcController(self):
        return self.rcControl
        