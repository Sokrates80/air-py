"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Jan 19 23:32:24 2016

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""


class ConfigFileGenerator:

    @classmethod
    def get_default_config_file(self):
        return {
            "num_motors": 4,
            "rcRadio": {
                'type': 'sbus',
                'calibrationStatus': False,
                'channels_default_center': [1024, 1024, 1024, 1024],
                'channels_default_min': [0, 0, 0, 0],
                'channels_default_max': [2047, 2047, 2047, 2047]
            }
        }