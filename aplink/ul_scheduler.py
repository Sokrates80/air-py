"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

22-Jan-2016 Initial Release

"""


class ULScheduler:

    def __init__(self):
        # Constants
        self.QOS_BYTE_INDEX = 4
        self.QOS_MAX_VALUE = 3
        self.QOS_BIT_MASK = 248  # First 5 bits 11111000 = 248

        # QOS Queue
        self.QCI0 = []
        self.QCI1 = []
        self.QCI2 = []
        self.QCI3 = []

        # Scheduler Parameters
        self.tmpQoS = 3
        self.QCI0Count = 0
        self.QCI1Count = 0
        self.QCI2Count = 0
        self.QCI3Count = 0

        self.QCI0_weight = 0.4
        self.QCI1_weight = 0.3
        self.QCI2_weight = 0.2
        self.QCI3_weight = 0.1

    def get_priority(self, qos_byte):
        self.tmpQoS = qos_byte & self.QOS_BIT_MASK >> 3

        if self.tmpQoS > self.QOS_MAX_VALUE:
            self.tmpQoS = self.QOS_MAX_VALUE  # for robustness against not supported QoS

        return self.tmpQoS

    def schedule_message(self, msg):
        print(self.get_priority(msg[self.QOS_BYTE_INDEX-1]))