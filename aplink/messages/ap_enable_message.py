"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

"""


class EnableMessage:

    MESSAGE_TYPE_ID = 40

    def __init__(self):
        pass

    @staticmethod
    def decode_payload(payload):
        """
        Used to enable the generation of a specific message type
        :param payload: the payload (bytearray) of the received packed
        :return: the decoded content of the packet; in this case the MESSAGE_TYPE_ID of the message to enable
        """
        return payload[0]
