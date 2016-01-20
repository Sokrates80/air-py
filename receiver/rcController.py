# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 23:32:24 2015

@author: fabrizioscimia

Revision History

13-Dec-2015 Initial Release
"""
from receiver.sbusReceiver import SBUSReceiver

class RCController:
    def __init__(self):
        #TODO select dynamically the receiver type
        self.rcCtrl = SBUSReceiver()
        print("RCController Started")
    
    def updateRxData(self):
        self.rcCtrl.getNewData()
    
    def getReport(self):
        report = self.rcCtrl.getRxReport()
        return report

    def getChannels(self):
        return self.rcCtrl.getRxChannels()

    def getChannel(self, num_channel):
        return self.rcCtrl.getRxChannel(num_channel-1) # convert from 0->n to 1->(n+1)

    def getLinkStatus(self):
        return self.rcCtrl.getFailsafeStatus()
        


