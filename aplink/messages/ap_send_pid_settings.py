"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

"""


class SendPIDSettings:

    MESSAGE_TYPE_ID = 90

    def __init__(self):
        """
        Used to trigger the generation of an ap_read_pid_settings message.
        :param h_builder: HeaderBuilder object
        :param attitude: AttitudeController object
        """
        pass

    @staticmethod
    def decode_payload(payload):
        return payload[0]
