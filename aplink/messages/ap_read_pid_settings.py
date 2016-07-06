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
import util.airpy_logger as logger


class ReadPID:

    MESSAGE_TYPE_ID = 100
    MESSAGE_KEY = 'ReadPID'

    def __init__(self, h_builder, attitude):
        """
        Used to carry the current PID settings as an array of 8 float:
        [stab_Kp,stab_Kd,stab_Ki,Max Increment,gyro_Kp,gyro_Kd,gyro_Ki,gyro_Max Increment]
        :param h_builder: HeaderBuilder object
        :param attitude: AttitudeController object
        """
        self.attitude_controller = attitude
        self.header_builder = h_builder
        self.QCI = 0
        self.floatList = self.attitude_controller.get_pid_settings()
        self.PAYLOAD_PID = struct.pack('%sf' % len(self.floatList), *self.floatList)
        self.PAYLOAD = bytearray(self.PAYLOAD_PID)
        self.PAYLOAD_LENGTH = len(self.PAYLOAD)
        self.EOF = bytearray([self.PAYLOAD[0] & 255])
        self.FAIL_SAFE = (self.attitude_controller.get_rc_controller()).get_link_status()
        self.header = bytearray(h_builder.get_header(self))
        self.message = self.header + self.PAYLOAD + self.EOF

    def get_bytes(self):
        return self.message
