"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sat Mar 12 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

12-Mar-2016 Initial Release

"""

import util.airpy_logger as logger


class DLReceiver:

    def __init__(self,apl_manager, streamer, h_builder):
        self.byte_streamer = streamer
        self.header_builder = h_builder
        self.aplink_manager = apl_manager
        self.tmpByte = None
        self.startByteFound = False
        self.byteIndex = 0
        self.messageId = 0
        self.CQI = 3
        self.lastFragment = 0
        self.messageTypeId = 0
        self.payloadLength = 0
        self.EOF = None
        self.payload = None

    def read_byte(self):
        # Read a new byte from the serial connection
        self.tmpByte = self.byte_streamer.read_byte()

        if self.tmpByte is not None:
            # logger.info("new incoming byte: {}, byteIndex: {}".format(self.tmpByte[0], self.byteIndex))
            if self.startByteFound:
                if self.byteIndex < self.header_builder.HEADER_LEN:
                    self.parse_header()
                else:
                    self.load_payload()
            else:
                if self.tmpByte[0] == 15:  # TODO change into constant
                    self.startByteFound = True
                    self.byteIndex += 1

    def parse_header(self):

        if self.byteIndex == 1:
            self.messageId = self.tmpByte[0] << 8

        elif self.byteIndex == 2:
            self.messageId += self.tmpByte[0]

        elif self.byteIndex == 3:
            self.CQI = self.tmpByte[0] & 0xF8 >> 3
            self.lastFragment = self.tmpByte[0] & 0x07

        elif self.byteIndex == 4:
            self.messageTypeId = self.tmpByte[0]

        elif self.byteIndex == 11:
            self.payloadLength = self.tmpByte[0]

        self.byteIndex += 1

    def load_payload(self):
        if self.byteIndex == self.header_builder.HEADER_LEN + self.payloadLength:

            if self.tmpByte[0] == self.EOF:
                logger.info("incoming message ready for decoding")
                self.decode_payload(self.messageTypeId, self.payload)
            else:
                logger.info("incoming message discarded")

            self.byteIndex = -1
            self.startByteFound = False

        elif self.byteIndex == self.header_builder.HEADER_LEN:  # 1st byte of the payload is replicated at the EOF
            self.EOF = self.tmpByte[0]
            self.payload = bytearray(self.payloadLength);
            self.payload[0] = self.tmpByte[0]

        else:
            self.payload[self.byteIndex-self.header_builder.HEADER_LEN] = self.tmpByte[0]

        self.byteIndex += 1

    def decode_payload(self, message_type_id, payload):

        if message_type_id == 40:
            self.aplink_manager.set_message_status(payload[0], 1)
        elif message_type_id == 50:
            self.aplink_manager.set_message_status(payload[0], 0)
