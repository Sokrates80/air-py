"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sat Mar 12 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

12-Mar-2016 Initial Release

"""

import util.airpy_logger as logger
from aplink.messages.ap_enable_message import EnableMessage
from aplink.messages.ap_disable_message import DisableMessage
from aplink.messages.ap_enable_esc_calibration import EnableEscCalibration
from aplink.messages.ap_save_pid_settings import SavePIDSettings
from aplink.messages.ap_read_pid_settings import ReadPID
from aplink.messages.ap_send_pid_settings import SendPIDSettings
from aplink.messages.ap_gyro_calibration import GyroCalibration
from util.airpy_config_utils import save_config_file, load_config_file


class DLReceiver:

    def __init__(self, apl_manager, streamer, h_builder):
        """
        This class is used to handle incoming APLINK messages received through the serial interface
        :param apl_manager: AplinkManager object
        :param streamer: airpy_byte_streamer object used to write on the serial interface
        :param h_builder: HeaderBuilder object used to generate the APLINK protocol Header
        """
        self.byte_streamer = streamer
        self.header_builder = h_builder
        self.aplink_manager = apl_manager
        self.tmpByte = None
        self.startByteFound = False
        self.byteIndex = 0
        self.messageId = 0
        self.QCI = 3
        self.lastFragment = 0
        self.messageTypeId = 0
        self.payloadLength = 0
        self.EOF = None
        self.payload = None

        # reporting
        self.valid_msg_count = 0
        self.discarded_msg_count = 0

    def read_byte(self):
        # Read a new byte from the serial connection
        self.tmpByte = self.byte_streamer.read_byte()

        if self.tmpByte is not None:

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

        if self.byteIndex == self.header_builder.MESSAGE_ID_BYTE_1:
            self.messageId = self.tmpByte[0] << 8

        elif self.byteIndex == self.header_builder.MESSAGE_ID_BYTE_2:
            self.messageId += self.tmpByte[0]

        elif self.byteIndex == self.header_builder.QCI_AND_LAST_FRAGMENT:
            self.QCI = (self.tmpByte[0] & 0xF8) >> 3
            self.lastFragment = self.tmpByte[0] & 0x07

        elif self.byteIndex == self.header_builder.MESSAGE_TYPE_ID:
            self.messageTypeId = self.tmpByte[0]

        elif self.byteIndex == self.header_builder.PAYLOAD_LENGTH:
            self.payloadLength = self.tmpByte[0]

        self.byteIndex += 1

    def load_payload(self):
        if self.byteIndex == self.header_builder.HEADER_LEN + self.payloadLength:

            if self.tmpByte[0] == self.EOF:
                self.decode_payload(self.messageTypeId, self.payload)
                self.valid_msg_count += 1

            else:
                self.discarded_msg_count += 1

            self.byteIndex = -1
            self.startByteFound = False

        elif self.byteIndex == self.header_builder.HEADER_LEN:  # 1st byte of the payload is replicated at the EOF
            self.EOF = self.tmpByte[0]
            self.payload = bytearray(self.payloadLength)
            self.payload[0] = self.tmpByte[0]

        else:
            self.payload[self.byteIndex-self.header_builder.HEADER_LEN] = self.tmpByte[0]

        self.byteIndex += 1

    def decode_payload(self, message_type_id, payload):

        if message_type_id == EnableMessage.MESSAGE_TYPE_ID:
            self.aplink_manager.set_message_status(EnableMessage.decode_payload(payload), 1)
        elif message_type_id == DisableMessage.MESSAGE_TYPE_ID:
            self.aplink_manager.set_message_status(EnableMessage.decode_payload(payload), 0)
        elif message_type_id == EnableEscCalibration.MESSAGE_TYPE_ID:
            EnableEscCalibration.enable_esc_calibration()
        elif message_type_id == SavePIDSettings.MESSAGE_TYPE_ID:
            pid_settings = SavePIDSettings.decode_payload(payload)
            config = load_config_file("config.json")
            config['attitude']['stab_Kp'] = pid_settings[0]
            config['attitude']['stab_Kd'] = pid_settings[1]
            config['attitude']['stab_Ki'] = pid_settings[2]
            config['attitude']['max_increment'] = pid_settings[3]
            config['attitude']['gyro_Kp'] = pid_settings[4]
            config['attitude']['gyro_Kd'] = pid_settings[5]
            config['attitude']['gyro_Ki'] = pid_settings[6]
            config['attitude']['max_gyro_increment'] = pid_settings[7]
            save_config_file("config.json", config)

            # Release the memory
            config = None

            # update current values
            self.aplink_manager.attitude.set_PID_settings(pid_settings)
        elif message_type_id == GyroCalibration.MESSAGE_TYPE_ID:

            if GyroCalibration.decode_payload(payload) == 10:  # start Calibration
                self.aplink_manager.attitude.gyro_calibration(False)
                logger.info("Gyro Calibration Started")
            elif GyroCalibration.decode_payload(payload) == 20:  # stop Calibration
                self.aplink_manager.attitude.gyro_calibration(True)
                logger.info("Gyro Calibration Completed")
        elif message_type_id == SendPIDSettings.MESSAGE_TYPE_ID:
            logger.info("Send PID Request Received")
            self.aplink_manager.new_message_from_key(ReadPID.MESSAGE_KEY)
            logger.info("PID Settings Sent")
