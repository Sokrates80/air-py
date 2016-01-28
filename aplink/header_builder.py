"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""

from aplink.messages.ap_heartbeat import Heartbeat
from aplink.messages.ap_rc_info import RcInfo

class HeaderBuilder:

    def __init__(self, config):

        # constants
        self.MESSAGE_ID_NUM_BIT = config['header']['message_id']['length_bit']
        self.FRAME_MARKER = b'\FF'
        self.HEADER_LEN = 40

        # class variables
        self.sequenceNumber = 0
        self.tempMessageID = 10858  # TODO to be retrieved randomly

    def get_message_id(self):
        return self.tempMessageID