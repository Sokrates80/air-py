"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

This class is used to serialize outgoing aplink messages

Revision History:

18-Feb-2016 Initial Release

"""

import util.airpy_logger as logger


class ULSerializer:
    def __init__(self, config, ulsched):

        # set uplink scheduler
        self.ul_scheduler = ulsched

        # buffer to store msg in the queue
        self.msg_buffer = bytearray(config['max_message_length'])

        # counter to track buffer occupancy
        self.bytes_in_buffer = 0
        self.byte_to_send_index = 0

        self.tmp_msg = None
        self.single_byte = bytearray(1)

        logger.info("UL Serializer loaded")

    def add_msg(self, msg):
        # self.msg_buffer += msg
        self.bytes_in_buffer = len(msg)
        self.byte_to_send_index = 0
        print("Serial Buffer Len:", len(self.msg_buffer))
        self.msg_buffer[0:self.bytes_in_buffer] = msg

    def read_queue(self):

        self.single_byte = bytearray(1)
        if self.bytes_in_buffer - self.byte_to_send_index == 0:
            self.tmp_msg = self.ul_scheduler.get_message()

            if self.tmp_msg is not None:
                self.add_msg(self.tmp_msg)
                print("New Message to Serialize")

        if self.bytes_in_buffer - self.byte_to_send_index > 0:
            # print("bytes_in_buffer", self.bytes_in_buffer, " - byte index:", self.byte_to_send_index, "msg:", self.msg_buffer[self.byte_to_send_index])
            self.single_byte[0] = self.msg_buffer[self.byte_to_send_index]
            self.byte_to_send_index += 1
        else:
            self.single_byte = None

        return self.single_byte
