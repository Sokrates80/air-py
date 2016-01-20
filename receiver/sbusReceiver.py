# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 23:32:24 2015

@author: fabrizioscimia

Revision History

13-Dec-2015 Initial Release
"""

from pyb import UART
import array
#import binascii

class SBUSReceiver:
        def __init__(self):
            self.sbus = UART(6,100000)
            self.sbus.init(100000,bits=8,parity=0,stop=2,timeout_char=3,read_buf_len=250)
            
            #constants
            self.START_BYTE = b'0f'
            self.END_BYTE = b'00'
            self.SBUS_FRAME_LEN = 25
            self.SBUS_NUM_CHAN = 18
            self.OUT_OF_SYNC_THD = 10
            self.SBUS_NUM_CHANNELS = 18
            self.SBUS_SIGNAL_OK = 0
            self.SBUS_SIGNAL_LOST = 1
            self.SBUS_SIGNAL_FAILSAFE = 2
            
            #Stack Variables initialization
            self.validSbusFrame = 0
            self.lostSbusFrame = 0
            self.frameIndex = 0
            self.resyncEvent = 0
            self.outOfSyncCounter = 0
            self.sbusBuff = bytearray(1) #single byte used for sync
            self.sbusFrame = bytearray(25) #single SBUS Frame
            self.sbusChannels = array.array('I', (0,)*self.SBUS_FRAME_LEN) #RC Channels
            self.isSync = False
            self.startByteFound = False
            self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE
            
            print("\n\rSBUS Stack Started")
        
        def getRxChannels(self):
            return self.sbusChannels

        def getRxChannel(self, num_ch):
            return self.sbusChannels[num_ch]

        def getFailsafeStatus(self):
            return self.failSafeStatus

        def getRxReport(self):
            
            rep = {}
            rep['Valid Frames'] = self.validSbusFrame
            rep['Lost Frames'] = self.lostSbusFrame
            rep['Resync Events'] = self.resyncEvent
            
            return rep
            
        def decodeFrame(self):
            
            for i in range(0, self.SBUS_NUM_CHANNELS-2):
                self.sbusChannels[i] = 0
                
            #counters initialization
            byteInSbus = 1
            bitInSbus = 0
            ch = 0
            bitInChannel = 0
            
            for i in range(0, 175): #TODO Generalzation
                if (self.sbusFrame[byteInSbus] & (1<<bitInSbus)):
                    self.sbusChannels[ch]|=(1<<bitInChannel)
                    #print(self.sbusChannels[ch], '\n\n')

                bitInSbus += 1
                bitInChannel += 1

                if bitInSbus == 8:
                    bitInSbus = 0
                    byteInSbus += 1

                if bitInChannel == 11:
                    bitInChannel = 0
                    ch += 1

            #Decode Digitals Channels

            #Digital Channel 1
            if (self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1<<0)):
                self.sbusChannels[self.SBUS_NUM_CHAN-2] = 1
            else:
                self.sbusChannels[self.SBUS_NUM_CHAN-2] = 0

            #Digital Channel 2
            if (self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1<<1)):
                self.sbusChannels[self.SBUS_NUM_CHAN-1] = 1
            else:
                self.sbusChannels[self.SBUS_NUM_CHAN-1] = 0

            #Failsafe
            self.failSafeStatus = self.SBUS_SIGNAL_OK
            if (self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1<<2)):
                self.failSafeStatus = self.SBUS_SIGNAL_LOST
            if (self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1<<3)):
                self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE


        def getSync(self):
            #print('Synchronizing..')
            if (self.sbus.any() > 0):

                if (self.startByteFound == True):
                    if (self.frameIndex == self.SBUS_FRAME_LEN - 1):
                        self.sbus.readinto(self.sbusBuff, 1) #end of frame byte
                        if (self.sbusBuff[0] == 0): #TODO: Change to use constant var value
                            self.startByteFound = False
                            self.isSync = True
                            self.frameIndex = 0
                    else:
                        self.sbus.readinto(self.sbusBuff, 1) #keep reading 1 byte until the end of frame
                        self.frameIndex += 1
                else:
                    self.frameIndex = 0
                    self.sbus.readinto(self.sbusBuff, 1) #read 1 byte
                    if (self.sbusBuff[0] == 15): #TODO: Change to use constant var value
                        self.startByteFound = True
                        self.frameIndex += 1
        

        def getNewData(self):

            if (self.isSync == True):
                if (self.sbus.any() >= self.SBUS_FRAME_LEN):
                    self.sbus.readinto(self.sbusFrame, self.SBUS_FRAME_LEN) #read the whole frame
                    if (self.sbusFrame[0] == 15 and self.sbusFrame[self.SBUS_FRAME_LEN-1] == 0): #TODO: Change to use constant var value
                        self.validSbusFrame += 1
                        self.outOfSyncCounter = 0
                        #decode the frame
                        self.decodeFrame()
                    else:
                        self.lostSbusFrame += 1
                        self.outOfSyncCounter += 1

                    if self.outOfSyncCounter > self.OUT_OF_SYNC_THD:
                        self.isSync = False
                        self.resyncEvent += 1
            else:
                self.getSync()