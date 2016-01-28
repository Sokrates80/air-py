"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

20-Jan-2016 Initial Release

"""

import array
import util.airpy_logger as logger


class ULMux:
    def __init__(self, config, ulsched):

        # set uplink scheduler
        self.ul_scheduler = ulsched

        # load ul mux config
        self.buffer_len = config['ul_mux']['buffer_len']

        # buffer to store msg in the queue
        self.msg_buffer = array.array('B', (0,)*self.buffer_len)  # TODO resize the buffer according to max msg len

        self.tmp_msg = None
        self.startIndex = 0
        self.endIndex = 0
        self.lostMsg = 0
        self.lock = False

        log_msg = "UL Mux loaded, BUFFER_SIZE = " + str(self.buffer_len)

        logger.info(log_msg)

    def add_msg(self, msg):

        self.lock = True  # lock is used to prevent fragmentation of different messages
        if self.startIndex <= self.endIndex:

            if ((self.endIndex + len(msg)) % len(self.msg_buffer) < self.startIndex) or \
                    (self.endIndex + len(msg) <= len(self.msg_buffer)-1):

                for i in range(0, len(msg)-1):
                    self.msg_buffer[(self.endIndex + i + 1) % len(self.msg_buffer)] = msg[i]

                self.endIndex = (self.endIndex + len(msg)) % len(self.msg_buffer)
            else:
                self.lostMsg += 1
        elif self.endIndex < self.startIndex:

            if (self.endIndex + len(msg)) < self.startIndex:

                for i in range(0, len(msg)-1):
                    self.msg_buffer[self.endIndex + i + 1] = msg[i]
                    self.endIndex += len(msg)
            else:
                self.lostMsg += 1
        self.lock = False

    def read_queue(self):
        if not self.lock:

            if self.startIndex == self.endIndex:

                # buffer is empty, load a new message TODO avoid waiting for the buffer to be empty
                single_byte = None
                self.tmp_msg = self.ul_scheduler.get_message()
                if self.tmp_msg is not None:
                    self.add_msg(self.tmp_msg)
            else:
                single_byte = self.msg_buffer[self.startIndex]
                if self.startIndex == len(self.msg_buffer)-1:
                    self.startIndex = 0
                else:
                    self.startIndex += 1
        else:
            single_byte = None
        return single_byte
