"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

20-Jan-2016 Initial Release

"""

import ujson

import util.airpy_logger as logger
from aplink.header_builder import HeaderBuilder
from aplink.ul_scheduler import ULScheduler
from aplink.dl_receiver import DLReceiver
from util.airpy_byte_streamer import airpy_byte_streamer

# Import message classes TODO import class dynamically based on the json config file
from aplink.messages.ap_heartbeat import Heartbeat
from aplink.messages.ap_rc_info import RcInfo
from aplink.messages.ap_imu import ImuStatus


class APLinkManager:
    def __init__(self, att_ct):

        # constants
        self.CONFIG_FILE_NAME = 'aplink_config.json'
        self.ENABLED = 1
        self.DISABLED = 0

        # load aplink config file
        self.aplink_config = self.load_aplink_config()

        # protocol states
        self.DISCONNECTED = 0
        self.CONNECTED = 1
        self.REPL = 2

        # init message triggers
        self.msg_triggers = {}
        self.min_tti = self.aplink_config['min_tti_ms']
        self.get_config_infos(self.aplink_config['messages'])
        self.tmp_msg = None

        # set attitude controller
        self.attitude = att_ct

        # set rc controller
        self.rc_controller = att_ct.get_rc_controller()

        # create header builder
        self.header_builder = HeaderBuilder(self.aplink_config)

        # create the Byte Streamer
        self.byte_streamer = airpy_byte_streamer()

        # create the Uplink Scheduler
        self.ul_scheduler = ULScheduler(self.aplink_config, self.byte_streamer)

        # create the DL Receiver
        self.dl_receiver = DLReceiver(self, self.byte_streamer, self.header_builder)

        self.message_factory = {
            'Heartbeat': Heartbeat,
            'RcInfo': RcInfo,
            'ImuStatus': ImuStatus
        }
        logger.info("aplink stack loaded successfully")
        #logger.debug("min tti:{}".format(self.min_tti))

    def load_aplink_config(self):
        config = None
        try:
            f = open(self.CONFIG_FILE_NAME, 'r')
            config = ujson.loads(f.readall())
            f.close()
            logger.info("aplink_config.json loaded successfully")
        except:
            logger.error("can't load aplink_config.json")
        return config

    def get_config_infos(self, messages):
        for key, value in messages.items():
            # calculate normalized triggers for each message
            self.msg_triggers.update({value['class']: {'message_type_id': value['message_type_id'],'enabled': value['enabled'], 'tti_ms': value['tti_ms']/self.min_tti, 'tti_count': 0}})
        # debug
        # for key, value in self.msg_triggers.items():
        #    logger.info("Key:{} Value:{}".format(key, value))

    def get_timer_freq(self):
        return 1000.0/self.min_tti

    def new_message(self):
        for key, value in self.msg_triggers.items():
            value['tti_count'] += 1
            if value['enabled'] == self.ENABLED:
                if value['tti_count'] >= value['tti_ms']:
                    #logger.debug("send_message - time to send: {}".format(key))
                    self.tmp_msg = self.message_factory[key](self.header_builder, self.attitude)
                    self.ul_scheduler.schedule_message(self.tmp_msg.get_bytes())
                    value['tti_count'] = 0

    def set_message_status(self, msg_type_id, new_status):
        for key, value in self.msg_triggers.items():
            if value['message_type_id'] == msg_type_id:
                value['enabled'] = new_status
