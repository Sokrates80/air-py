"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Jan 19 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release

"""

import pyb
import ujson
from config.configFileGenerator import ConfigFileGenerator

class ConfigFileManager:

    def __init__(self):
        self.CONFIG_FILE_NAME = 'config.json'
        self.configFile = None
        self.loadConfigFile()
        print('ConfigFileManager Started')

    def loadConfigFile(self):
        try:
            f = open(self.CONFIG_FILE_NAME, 'r')
            self.configFile = ujson.loads(f.readall())
            f.close()
        except:
            self.createDefaultConfig()

    def createDefaultConfig(self):
        conf = ConfigFileGenerator()
        try:
            f = open('config.json', 'w')
            f.write(ujson.dumps(conf.getDefaultConfiFile()))
            f.close()
        except:
            c = 1 #TODO Log Error

        return conf.getDefaultConfiFile()


