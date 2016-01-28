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
from aplink.ul_mux import ULMux
from aplink.ul_scheduler import ULScheduler

# Import message classes TODO import class dynamically based on the json config file
from aplink.messages.ap_heartbeat import Heartbeat
from aplink.messages.ap_rc_info import RcInfo

class APLinkManager:
    def __init__(self, att_ct):

        # constants
        self.CONFIG_FILE_NAME = 'aplink_config.json'

        # load aplink config file
        self.aplink_config = self.load_aplink_config()

        # init message triggers
        self.msg_triggers = {}  # TODO load all message triggers. USE a factory?
        self.min_tti = 10000    # TODO use a proper init value
        self.get_config_infos(self.aplink_config['messages'])  # TODO set aplink timer according with min tti
        self.min_tti_count = 0

        # set attitude controller
        self.attitude = att_ct

        # set rc controller
        self.rc_controller = att_ct.get_rc_controller()

        # create header builder
        self.header_builder = HeaderBuilder(self.aplink_config)

        # create the Uplink Scheduler
        self.ul_scheduler = ULScheduler(self.aplink_config)

        # create the Uplink Mux
        self.ul_mux = ULMux(self.aplink_config, self.ul_scheduler)

        # debug
        self.test = Heartbeat(self.header_builder, self.attitude)
        print('min tti:', self.min_tti, ' heartbeat:', self.test)
        logger.info("aplink stack loaded successfully")

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
            #print(value['tti_ms'])
            #self.msg_modules.append(value['module'])
            if value['tti_ms'] < self.min_tti:
                self.min_tti = value['tti_ms']

    def send_message(self):
        self.min_tti_count += 1
