"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""


class Heartbeat:
    def __init__(self):
        self.QCI = 0
        self.MESSAGE_TYPE_ID = 1
        self.PAYLOAD_LENGTH = 1
        self.PAYLOAD = b'FF'
