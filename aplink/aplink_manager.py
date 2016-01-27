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
    def __init__(self):

        # constants
        self.CONFIG_FILE_NAME = 'aplink_config.json'

        # load aplink config file
        self.aplink_config = self.load_aplink_config()

        # load header builder
        self.header_builder = HeaderBuilder(self.aplink_config)

        # create the Uplink Mux
        self.ul_mux = ULMux(self.aplink_config)

        # create the Uplink Scheduler
        self.ul_scheduler = ULScheduler(self.aplink_config, self.ul_mux)

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
