"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

This class is used to schedule outgoing protocol messages according to their priority

Revision History:

22-Jan-2016 Initial Release

"""

import util.airpy_logger as logger
import array
import gc


class ULScheduler:
    def __init__(self, config):

        # Scheduler Settings
        self.QCI_BYTE_INDEX = config['header']['qci']['index']
        self.QCI_MAX_VALUE = config['ul_scheduler']['QCI_max']
        self.QCI0_weight = config['ul_scheduler']['QCI0_weight']
        # self.QCI1_weight = config['ul_scheduler']['QCI1_weight']
        # self.QCI2_weight = config['ul_scheduler']['QCI2_weight']
        # self.QCI3_weight = config['ul_scheduler']['QCI3_weight']
        self.QCI0_buff_len = 1500  # TODO dynamically allocate the buffer size based on config
        self.QCI0_msg_size_len = 20  # TODO dynamically allocate the buffer size based on config
        self.tmpQCI = 3
        self.QCI_BIT_MASK = 248  # First 5 bits 11111000 = 248
        self.tmp_msg = None

        # QOS Queues containing ap messages according to the related QCI

        self.QCI0_buff = array.array('B', (0,) * self.QCI0_buff_len)
        self.QCI0_msg_len = array.array('I', (0,) * self.QCI0_msg_size_len)
        self.QCI0_index = 0
        # self.QCI1 = []
        # self.QCI2 = []
        # self.QCI3 = []
        # self.QCI_queue = [self.QCI0, self.QCI1, self.QCI2, self.QCI3]
        # self.QCI_queues = {
        #    'QCI0': {'buffer': self.QCI0_buff, 'msg_len': self.QCI0_msg_len, 'index': 0}
        # }

        # Scheduler Parameters
        self.QCI0Count = 0
        # self.QCI1Count = 0
        # self.QCI2Count = 0
        # self.QCI3Count = 0

        log_msg = "UL Scheduler loaded, QCI weights = " + str(self.QCI0_weight)
        # log_msg += ',' + str(self.QCI1_weight)+',' + str(self.QCI2_weight) + ',' + str(self.QCI3_weight)

        logger.info(log_msg)

    def schedule_message(self, msg):
        # TODO handle msg discarding if buffer is full
        self.tmpQCI = msg[self.QCI_BYTE_INDEX] & self.QCI_BIT_MASK >> 3

        if self.tmpQCI > self.QCI_MAX_VALUE:
            self.tmpQCI = self.QCI_MAX_VALUE  # for robustness against not supported QoS

        # TODO handling of other queues
        for j in range(0, len(msg)):
            self.QCI0_buff[self.QCI0_index + j] = msg[j]
        self.QCI0_msg_len[self.QCI0Count] = len(msg)
        self.QCI0_index += len(msg)
        self.QCI0Count += 1

    def get_message(self):

        # TODO select the right queue based on the weight
        self.tmp_msg = None

        if self.QCI0Count > 0:
            self.tmp_msg = self.QCI0_buff[0:self.QCI0_msg_len[0]]
            logger.debug("Range:{} - msg in queue:{} - index:{}".format(self.QCI0_index-self.QCI0_msg_len[0],
                                                                        self.QCI0Count,
                                                                        self.QCI0_index))
            for k in range(0, self.QCI0_index-self.QCI0_msg_len[0]):
                self.QCI0_buff[k] = self.QCI0_buff[self.QCI0_msg_len[0] + k]
            # shift array on the left by 1
            for i in range(0, self.QCI0Count):
                self.QCI0_msg_len[i] = self.QCI0_msg_len[i+1]
            self.QCI0_index -= len(self.tmp_msg)
            self.QCI0Count -= 1
        else:
            self.QCI0_index = 0
            self.QCI0_msg_len[0] = 0

        return self.tmp_msg
