"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

28-Jan-2016 Initial Release

"""


class RcInfo:
    def __init__(self, h_builder, attitude):
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 1
        self.PAYLOAD_LENGTH = 1
        self.PAYLOAD = b'FF'
        self.attitude_controller = attitude
        self.header_builder = h_builder
