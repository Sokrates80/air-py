"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""
# import binascii

class Heartbeat:
    def __init__(self, h_builder, attitude):
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 10
        self.PAYLOAD_LENGTH = 1
        self.PAYLOAD = [255]
        self.EOF = [255]
        self.attitude_controller = attitude
        self.header_builder = h_builder
        self.FAIL_SAFE = (self.attitude_controller.get_rc_controller()).get_link_status()
        self.header = bytearray(h_builder.get_header(self))
        self.message = self.header + bytearray(self.PAYLOAD) + bytearray(self.EOF)

    def get_bytes(self):
        # print("Len message HBeat:", len(self.message), " - Message: ", binascii.hexlify(self.message), " - PAY_LEN:", self.PAYLOAD_LENGTH)
        return self.message



