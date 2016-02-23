"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

28-Jan-2016 Initial Release

"""
# import binascii


class RcInfo:
    def __init__(self, h_builder, attitude):

        self.attitude_controller = attitude
        self.header_builder = h_builder
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 20
        self.PAYLOAD = bytearray((self.attitude_controller.get_rc_controller()).get_channels())
        self.PAYLOAD_LENGTH = len(self.PAYLOAD)  # Short = 2 Bytes TODO: get size in bytes
        self.EOF = bytearray([self.PAYLOAD[0] & 255])
        self.FAIL_SAFE = (self.attitude_controller.get_rc_controller()).get_link_status()
        self.header = bytearray(h_builder.get_header(self))
        self.message = self.header + self.PAYLOAD + self.EOF

    def get_bytes(self):
        # print("Len message RC:", len(self.message), " - Message: ", binascii.hexlify(self.message), " - PAY_LEN:", self.PAYLOAD_LENGTH, "- EOD_LEN: ", len(self.EOF))
        return self.message



