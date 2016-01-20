"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Jan 19 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release

"""

import ujson
from config.config_file_generator import ConfigFileGenerator


class ConfigFileManager:
    def __init__(self):
        self.CONFIG_FILE_NAME = 'config.json'
        self.configFile = None
        self.load_config_file()
        print('ConfigFileManager Started')

    def load_config_file(self):
        try:
            f = open(self.CONFIG_FILE_NAME, 'r')
            self.configFile = ujson.loads(f.readall())
            f.close()
        except:
            self.create_default_config()

    def create_default_config(self):
        conf = ConfigFileGenerator()
        try:
            f = open('config.json', 'w')
            f.write(ujson.dumps(conf.get_default_config_file()))
            f.close()
        except:
            c = 1  # TODO Log Error

        return conf.get_default_config_file()
