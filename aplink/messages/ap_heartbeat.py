"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""


class Heartbeat:
    def __init__(self, h_builder, attitude):
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 10
        self.PAYLOAD_LENGTH = 1
        self.PAYLOAD = b'\xFF'
        self.EOF = b'\xFF'
        self.attitude_controller = attitude
        self.header_builder = h_builder
        self.header = bytearray(h_builder.get_header(self))
        self.message = self.header + bytearray(self.PAYLOAD)

    def get_bytes(self):
        return self.message



