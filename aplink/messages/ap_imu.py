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

# TODO split this message into two: IMU and MOTORS


class ImuStatus:
    def __init__(self, h_builder, attitude):
        """
        This message is used to carry IMU and MOTOR related information:
        IMU: 6 float in total (3 for Pitch,Roll,Yaw angles and 3 for the related angular velocities)
        MOTORS: 4 float in total (1 for each motor PWM value)
        :param h_builder: HeaderBuilder object
        :param attitude: AttitudeController object
        """

        self.attitude_controller = attitude
        self.header_builder = h_builder
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 30
        self.floatList = self.attitude_controller.get_attitude_status()
        self.shortlist = self.attitude_controller.get_pulse_widths()
        self.PAYLOAD_IMU = struct.pack('%sf' % len(self.floatList), *self.floatList)
        self.PAYLOAD_MOTORS = struct.pack('%sH' % len(self.shortlist), *self.shortlist)
        self.PAYLOAD = bytearray(self.PAYLOAD_IMU) + bytearray(self.PAYLOAD_MOTORS)
        self.PAYLOAD_LENGTH = len(self.PAYLOAD)
        self.EOF = bytearray([self.PAYLOAD[0] & 255])
        self.FAIL_SAFE = (self.attitude_controller.get_rc_controller()).get_link_status()
        self.header = bytearray(h_builder.get_header(self))
        self.message = self.header + self.PAYLOAD + self.EOF

    def get_bytes(self):
        return self.message
