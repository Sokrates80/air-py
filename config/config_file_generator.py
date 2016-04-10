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
            "attitude": {
                'max_increment': 0.25,
                'max_pitch': 10,
                'max_roll': 10,
                'Kp': 1.5,
                'Kd': 0.05,
                'Ki': 0
            },
            "rcRadio": {
                'type': 'sbus',
                'calibrationStatus': False,
                'channels_default_center': [1024, 1024, 1024, 1024],
                'channels_default_min': [0, 0, 0, 0],
                'channels_default_max': [2047, 2047, 2047, 2047]
            },
            "esc": {
                "esc_pwm_min_cmd": 1000,
                "esc_pwm_center": 1500,
                "esc_pwm_min": 1150,
                "esc_pwm_max": 2000,
                "quadcopter": {
                  "pins": ["X1", "X2", "X3", "X4"],
                  "timers": [5, 5, 5, 5],
                  "channels": [1, 2, 3, 4]
                }
            }
        }
