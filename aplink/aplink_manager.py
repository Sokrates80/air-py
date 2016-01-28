"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

20-Jan-2016 Initial Release

"""

import ujson
import util.airpy_logger as logger
from aplink.ul_mux import ULMux
from aplink.ul_scheduler import ULScheduler
from aplink.messages.header_builder import HeaderBuilder


class APLinkManager:
    def __init__(self, att_ct):

        # constants
        self.CONFIG_FILE_NAME = 'aplink_config.json'

        # load aplink config file
        self.aplink_config = self.load_aplink_config()

        # init message triggers
        self.msg_triggers = {}  # TODO load all message triggers. USE a factory?
        self.min_tti = 10000    # TODO use a proper init value
        self.get_min_tti(self.aplink_config['timers'])  # TODO set timer according with min tti

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

        print('min tti:', self.min_tti)
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

    #def new_aplink_message(self):

    def get_min_tti(self, timers):
        for key, value in timers.items():
            #print(value['tti_ms'])
            if value['tti_ms'] < self.min_tti:
                self.min_tti = value
