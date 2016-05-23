"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Apr 10 17:11:24 2016

@author: Fabrizio Scimia

"""
import struct
import binascii
import util.airpy_logger as logger


class GyroCalibration:

    MESSAGE_TYPE_ID = 80

    def __init__(self):
        pass

    @staticmethod
    def decode_payload(payload):
        return payload[0]
