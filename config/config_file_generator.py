"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Jan 19 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""


class ConfigFileGenerator:
    def __init__(self):
        self.config = {}
        self.config['rcRadio'] = {}
        self.config['rcRadio']['type'] = 'sbus'
        self.config['rcRadio']['calibrationStatus'] = False
        self.config['rcRadio']['channels_default_center'] = [1024, 1024, 1024, 1024]
        self.config['rcRadio']['channels_default_min'] = [0, 0, 0, 0]
        self.config['rcRadio']['channels_default_max'] = [2047, 2047, 2047, 2047]

    def get_default_config_file(self):
        return self.config
