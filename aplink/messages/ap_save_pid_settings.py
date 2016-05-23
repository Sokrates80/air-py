"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Apr 10 17:11:24 2016

@author: Fabrizio Scimia

"""
import struct
import binascii
import util.airpy_logger as logger


class SavePIDSettings:

    MESSAGE_TYPE_ID = 70

    def __init__(self):
        pass

    @staticmethod
    def decode_payload(payload):
        """
        Decode message payload
        :param payload: byte stream representing the message payload
        :return: an array of float [Kp,Kd,Ki,Max Increment]
        """
        pid_settings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for i in range(0, 8):
            pid_settings[i] = struct.unpack('>f', payload[i*4:i*4 + 4])[0]

        return pid_settings
