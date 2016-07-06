"""
airPy is a flight controller based on pyboard and written in micropython.

The MIT License (MIT)
Copyright (c) 2016 Fabrizio Scimia, fabrizio.scimia@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import array


class HeaderBuilder:

    def __init__(self):
        """
        Used for dynamic Header generation
        """
        # constants
        # self.MESSAGE_ID_NUM_BIT = config['header']['message_id']['length_bit']
        self.FRAME_MARKER = b'\FF'
        self.HEADER_LEN = 12  # bytes
        self.SECOND_BYTE_BITMASK = 65280
        self.FIRST_BYTE_BITMASK = 255
        self.LAST_FRAGMENT_TRUE = 7
        self.LAST_FRAGMENT_FALSE = 0

        # header bytes index
        self.START_BYTE = 0
        self.MESSAGE_ID_BYTE_1 = 1
        self.MESSAGE_ID_BYTE_2 = 2
        self.QCI_AND_LAST_FRAGMENT = 3
        self.MESSAGE_TYPE_ID = 4
        self.LINK_ID = 5
        self.FRAGMENT_NUM_BYTE_1 = 6
        self.FRAGMENT_NUM_BYTE_2 = 7
        self.SEQUENCE_NUM_BYTE_1 = 8
        self.SEQUENCE_NUM_BYTE_2 = 9
        self.FAIL_SAFE_AND_FLIGHT_MODE = 10
        self.PAYLOAD_LENGTH = 11

        # class variables
        self.sequenceNumber = 0
        self.tempMessageID = 10858  # TODO to be retrieved randomly
        self.header = array.array('B', (0,) * self.HEADER_LEN)  # RC Channels
        self.tmp_message = None

    def get_header(self, msg):
        self.tmp_message = msg
        if self.tempMessageID == 65535:
            self.tempMessageID = 0
        else:
            self.tempMessageID += 1  # TODO change to be retrieved randomly
        self.build_header()
        return self.header

    def build_header(self):
        self.header[self.START_BYTE] = 15  # \x0F
        self.header[self.MESSAGE_ID_BYTE_1] = (self.tempMessageID & self.SECOND_BYTE_BITMASK) >> 8
        self.header[self.MESSAGE_ID_BYTE_2] = self.tempMessageID & self.FIRST_BYTE_BITMASK
        self.header[self.QCI_AND_LAST_FRAGMENT] = (self.tmp_message.QCI & self.FIRST_BYTE_BITMASK << 3) + (self.LAST_FRAGMENT_TRUE & self.FIRST_BYTE_BITMASK)
        self.header[self.MESSAGE_TYPE_ID] = self.tmp_message.MESSAGE_TYPE_ID & self.FIRST_BYTE_BITMASK
        self.header[self.LINK_ID] = 0  # Link ID TODO TB implemented
        self.header[self.FRAGMENT_NUM_BYTE_1] = 0  # Fragment Number Byte 1 TODO TB implemented
        self.header[self.FRAGMENT_NUM_BYTE_2] = 0  # Fragment Number Byte 2 TODO TB implemented
        self.header[self.SEQUENCE_NUM_BYTE_1] = 0  # Sequence Number Byte 1 TODO TB implemented
        self.header[self.SEQUENCE_NUM_BYTE_2] = 0  # Sequence Number Byte 2 TODO TB implemented
        self.header[self.FAIL_SAFE_AND_FLIGHT_MODE] = (self.tmp_message.FAIL_SAFE & self.FIRST_BYTE_BITMASK) << 4  # Failsafe & Flight Mode TODO Flight Mode TB implemented
        self.header[self.PAYLOAD_LENGTH] = self.tmp_message.PAYLOAD_LENGTH & self.FIRST_BYTE_BITMASK
