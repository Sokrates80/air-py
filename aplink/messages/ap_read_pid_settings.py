"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

28-Jan-2016 Initial Release

"""
import struct
import util.airpy_logger as logger


class ReadPID:

    MESSAGE_TYPE_ID = 100
    MESSAGE_KEY = 'ReadPID'

    def __init__(self, h_builder, attitude):

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
        #logger.info(self.floatList)
        return self.message
