"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""

import array


class HeaderBuilder:

    def __init__(self, config):

        # constants
        self.MESSAGE_ID_NUM_BIT = config['header']['message_id']['length_bit']
        self.FRAME_MARKER = b'\FF'
        self.HEADER_LEN = 13  # bytes
        self.MESSAGE_ID_BIT_MASK_B1 = 65280
        self.MESSAGE_ID_BIT_MASK_B2 = 255
        self.LAST_FRAGMENT_TRUE = 7
        self.LAST_FRAGMENT_FALSE = 0

        # class variables
        self.sequenceNumber = 0
        self.tempMessageID = 10858  # TODO to be retrieved randomly
        self.header = array.array('B', (0,) * self.HEADER_LEN)  # RC Channels
        self.tmp_message = None

    def get_header(self,msg):
        self.tmp_message = msg
        self.tempMessageID += 1  # TODO change to be retrieved randomly
        self.build_header()
        return self.header

    def build_header(self):
        self.header[0] = 15
        self.header[1] = (self.tempMessageID & self.MESSAGE_ID_BIT_MASK_B1) >> 8
        self.header[2] = self.tempMessageID & self.MESSAGE_ID_BIT_MASK_B2
        self.header[3] = self.tmp_message.QCI << 3 + self.LAST_FRAGMENT_TRUE
        self.header[4] = self.tmp_message.MESSAGE_TYPE_ID
        self.header[5] = 0  # Link ID TODO TB implemented
        self.header[6] = 0  # Fragment Number Byte 1 TODO TB implemented
        self.header[7] = 0  # Fragment Number Byte 2 TODO TB implemented
        self.header[8] = 0  # Sequence Number Byte 1 TODO TB implemented
        self.header[9] = 0  # Sequence Number Byte 2 TODO TB implemented
        self.header[10] = 0  # Failsafe & Flight Mode TODO TB implemented
        self.header[11] = self.tmp_message.PAYLOAD_LENGTH
        self.header[12] = self.tmp_message.EOF  # EOF = 1st Payload Byte
        # self.header[12] = 255  # EOF = 1st Payload Byte TODO TB implemented




