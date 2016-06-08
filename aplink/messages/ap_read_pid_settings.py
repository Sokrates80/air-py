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
