"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Jan 19 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""

from config.config_file_generator import ConfigFileGenerator
from util.airpy_config_utils import load_config_file, save_config_file
import util.airpy_logger as logger


class ConfigFileManager:

    CONFIG_FILE_NAME = 'config.json'

    def __init__(self):
        try:
            self.configFile = load_config_file(self.CONFIG_FILE_NAME)
        except:
            self.configFile = ConfigFileGenerator.get_default_config_file()
            save_config_file(self.CONFIG_FILE_NAME, self.configFile)

        logger.info('ConfigFileManager Started')
