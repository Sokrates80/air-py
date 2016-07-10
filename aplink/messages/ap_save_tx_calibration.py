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

import struct


class SaveTxCalibration:

    MESSAGE_TYPE_ID = 110

    def __init__(self):
        pass

    @staticmethod
    def decode_payload(payload):
        """
        Decode message payload
        :param payload: byte stream representing the message payload
        :return: a list of 3 list of integers representing the PWM threshold values for each of the N active channels
         [<min threshold values>,<max threshold values>, <center threshold values>]
        """

        # 4 byte per integer * 3 set of thesholds
        byte_per_thd_set = int(len(payload)/3)
        min_thd_vals = [0 for i in range(0, int(byte_per_thd_set/4))]
        max_thd_vals = [0 for i in range(0, int(byte_per_thd_set/4))]
        center_thd_vals = [0 for i in range(0, int(byte_per_thd_set/4))]

        for i in range(0, int(byte_per_thd_set/4)):
            min_thd_vals[i] = struct.unpack('>i', payload[i*4:i*4 + 4])[0]

        for i in range(0, int(byte_per_thd_set/4)):
            max_thd_vals[i] = struct.unpack('>i', payload[byte_per_thd_set + i*4:i*4 + 4 + byte_per_thd_set])[0]

        for i in range(0, int(byte_per_thd_set/4)):
            center_thd_vals[i] = struct.unpack('>i', payload[2*byte_per_thd_set + i*4:i*4 + 2*byte_per_thd_set + 4])[0]

        return [min_thd_vals, max_thd_vals, center_thd_vals]
