"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""


class HeaderBuilder:

    def __init__(self):
        # constants
        self.MESSAGE_ID_NUM_BYTES = 2
        self.FRAME_MARKER = b'\FF'

        # class variables
        self.sequenceNumber = 0
        self.tempMessageID = 0

    def get_message_id(self):
        return self.tempMessageID

