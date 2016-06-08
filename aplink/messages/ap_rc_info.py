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
        """
        Used to carry the decoded RC channels decoded value. The streaming of this message is enabled during the
        Tx calibration in order to set the min/max/centre value for each channel.
        It will carry 18 short values representing 18 SBUS channels (2 of that being digital)
        :param h_builder: HeaderBuilder object
        :param attitude: AttitudeController object
        """

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
        return self.message
