# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
 
"""

import pyb
import sys
from attitude.attitudeController import AttitudeController
from receiver.rcController import RCController
from config.configFileManager import ConfigFileManager
import micropython
import util.airpy_logger as logger

#for better callback related error reporting 
micropython.alloc_emergency_exception_buf(100)

updateLed = False
updateRx = False

led = pyb.LED(4)
logger.init(logger.AIRPY_INFO)

def statusLed(tim1):
    global updateLed
    updateLed=True
    led.toggle()
    
def updateRxData(timRx):
    global updateRx
    updateRx = True

def printReport():
    r = rcCtrl.getReport()
    sRep = str('Valid Frames: ') + str(r['Valid Frames']) + str(' - Lost Frames: ') + str(r['Lost Frames'])
    sRep += str(' - CH1: ') + str(rcCtrl.getChannel(1)) + str(', CH2: ') + str(rcCtrl.getChannel(2))
    sRep += str(', CH3: ') + str(rcCtrl.getChannel(3)) + str(', CH4: ') + str(rcCtrl.getChannel(4))
    sRep += str(' - Failsafe: ') + str(rcCtrl.getLinkStatus())
    logger.AIRPY_INFO(sRep)

    print(sRep)
    #sys.stdout.write(sRep + '    \r')
  
#Init Timer for status led and report  
tim1 = pyb.Timer(1)
tim1.init(freq=1)
tim1.callback(statusLed)

#Init Rx Timing at 300us (Frsky specific). TODO: Read RxTiming from Setting
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(updateRxData)

print("\n\rAirPy v0.0.1 booting...\n\r")

cm = ConfigFileManager()
config = cm.configFile
rcCtrl = RCController()
attitudeCtrl = AttitudeController()
attitudeCtrl.setRcController(rcCtrl)

while True: 
    if updateRx == True:
       rcCtrl.updateRxData()
       updateRx = False
    if updateLed == True:
       printReport(); 
       updateLed=False
        
    
        
    
    






