"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

This class is used to schedule outgoing protocol messages according to their priority

Revision History:

22-Jan-2016 Initial Release

"""

from aplink.ul_mux import ULMux
import util.airpy_logger as logger


class ULScheduler:
    def __init__(self, config, ulmux):

        # set Uplink Mux
        assert isinstance(ulmux, ULMux)
        self.ul_mux = ulmux

        # Scheduler Settings
        self.QCI_BYTE_INDEX = config['header']['qci']['index']
        self.QCI_MAX_VALUE = config['ul_scheduler']['QCI_max']
        self.QCI0_weight = config['ul_scheduler']['QCI0_weight']
        self.QCI1_weight = config['ul_scheduler']['QCI1_weight']
        self.QCI2_weight = config['ul_scheduler']['QCI2_weight']
        self.QCI3_weight = config['ul_scheduler']['QCI3_weight']
        self.tmpQoS = 3
        self.QCI_BIT_MASK = 248  # First 5 bits 11111000 = 248

        # QOS Queues containing ap messages according to the related QCI
        self.QCI0 = []
        self.QCI1 = []
        self.QCI2 = []
        self.QCI3 = []
        self.QCI_queue = [self.QCI0, self.QCI1, self.QCI2, self.QCI3]

        # Scheduler Parameters
        self.QCI0Count = 0
        self.QCI1Count = 0
        self.QCI2Count = 0
        self.QCI3Count = 0
        self.QCI_queues_count = [self.QCI0Count, self.QCI1Count, self.QCI2Count, self.QCI3Count]

        log_msg = "UL Scheduler loaded, QCI weights = " + str(self.QCI0_weight) + ',' + str(self.QCI1_weight)
        log_msg += ',' + str(self.QCI2_weight) + ',' + str(self.QCI3_weight)

        logger.info(log_msg)

    def schedule_message(self, msg):
        self.tmpQoS = msg[self.QCI_BYTE_INDEX] & self.QCI_BIT_MASK >> 3

        if self.tmpQoS > self.QCI_MAX_VALUE:
            self.tmpQoS = self.QCI_MAX_VALUE  # for robustness against not supported QoS

        #print(self.get_qos(msg[self.QCI_BYTE_INDEX]))
        self.QCI_queue[self.tmpQoS].append(msg)
        self.QCI_queues_count[self.tmpQoS] += 1

        #the approach is for each new scheduled message another message is sent to the mux TODO TBC
        self.send_message()

    def send_message(self):
        # TODO select the right queue
        if len(self.QCI_queue[0]) > 0:
            self.ul_mux.add_msg(self.QCI_queue[0].pop(0))
        self.QCI_queues_count[0] -= 1
