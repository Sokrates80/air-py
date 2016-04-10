# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""

from pyb import UART
import array
import util.airpy_logger as logger

class SBUSReceiver:
    def __init__(self):
        self.sbus = UART(3, 100000)
        self.sbus.init(100000, bits=8, parity=0, stop=2, timeout_char=3, read_buf_len=250)

        # constants
        self.START_BYTE = b'0f'
        self.END_BYTE = b'00'
        self.SBUS_FRAME_LEN = 25
        self.SBUS_NUM_CHAN = 18
        self.OUT_OF_SYNC_THD = 10
        self.SBUS_NUM_CHANNELS = 18
        self.SBUS_SIGNAL_OK = 0
        self.SBUS_SIGNAL_LOST = 1
        self.SBUS_SIGNAL_FAILSAFE = 2

        # Stack Variables initialization
        self.validSbusFrame = 0
        self.lostSbusFrame = 0
        self.frameIndex = 0
        self.resyncEvent = 0
        self.outOfSyncCounter = 0
        self.sbusBuff = bytearray(1)  # single byte used for sync
        self.sbusFrame = bytearray(25)  # single SBUS Frame
        self.sbusChannels = array.array('H', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # RC Channels
        self.isSync = False
        self.startByteFound = False
        self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

        logger.info("SBUS Stack Started")

    def get_rx_channels(self):
        return self.sbusChannels

    def get_rx_channel(self, num_ch):
        return self.sbusChannels[num_ch]

    def get_failsafe_status(self):
        return self.failSafeStatus

    def get_rx_report(self):

        rep = {}
        rep['Valid Frames'] = self.validSbusFrame
        rep['Lost Frames'] = self.lostSbusFrame
        rep['Resync Events'] = self.resyncEvent

        return rep

    def decode_frame(self):

        for i in range(0, self.SBUS_NUM_CHANNELS - 2):
            self.sbusChannels[i] = 0

        # counters initialization
        byte_in_sbus = 1
        bit_in_sbus = 0
        ch = 0
        bit_in_channel = 0

        for i in range(0, 175):  # TODO Generalization
            if self.sbusFrame[byte_in_sbus] & (1 << bit_in_sbus):
                self.sbusChannels[ch] |= (1 << bit_in_channel)

            bit_in_sbus += 1
            bit_in_channel += 1

            if bit_in_sbus == 8:
                bit_in_sbus = 0
                byte_in_sbus += 1

            if bit_in_channel == 11:
                bit_in_channel = 0
                ch += 1

        # Decode Digitals Channels

        # Digital Channel 1
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 0):
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 0

        # Digital Channel 2
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 1):
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 0

        # Failsafe
        self.failSafeStatus = self.SBUS_SIGNAL_OK
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 2):
            self.failSafeStatus = self.SBUS_SIGNAL_LOST
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 3):
            self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

    def get_sync(self):

        if self.sbus.any() > 0:

            if self.startByteFound:
                if self.frameIndex == (self.SBUS_FRAME_LEN - 1):
                    self.sbus.readinto(self.sbusBuff, 1)  # end of frame byte
                    if self.sbusBuff[0] == 0:  # TODO: Change to use constant var value
                        self.startByteFound = False
                        self.isSync = True
                        self.frameIndex = 0
                else:
                    self.sbus.readinto(self.sbusBuff, 1)  # keep reading 1 byte until the end of frame
                    self.frameIndex += 1
            else:
                self.frameIndex = 0
                self.sbus.readinto(self.sbusBuff, 1)  # read 1 byte
                if self.sbusBuff[0] == 15:  # TODO: Change to use constant var value
                    self.startByteFound = True
                    self.frameIndex += 1

    def get_new_data(self):

        if self.isSync:
            if self.sbus.any() >= self.SBUS_FRAME_LEN:
                self.sbus.readinto(self.sbusFrame, self.SBUS_FRAME_LEN)  # read the whole frame
                if (self.sbusFrame[0] == 15 and self.sbusFrame[
                        self.SBUS_FRAME_LEN - 1] == 0):  # TODO: Change to use constant var value
                    self.validSbusFrame += 1
                    self.outOfSyncCounter = 0
                    self.decode_frame()
                else:
                    self.lostSbusFrame += 1
                    self.outOfSyncCounter += 1

                if self.outOfSyncCounter > self.OUT_OF_SYNC_THD:
                    self.isSync = False
                    self.resyncEvent += 1
        else:
            self.get_sync()
