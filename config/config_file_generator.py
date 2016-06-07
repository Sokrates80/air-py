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
                'max_increment': 50,
                'max_gyro_increment': 50,
                'max_pitch': 45,
                'max_roll': 45,
                'max_yaw': 180,
                'stab_Kp': 1,
                'stab_Kd': 0,
                'stab_Ki': 0,
                'gyro_Kp': 1,
                'gyro_Kd': 0,
                'gyro_Ki': 0,
                'pitch_offset': -0.1,
                'roll_offset': -0.75,
                'pitch_rate_offset': 0.2,
                'roll_rate_offset': 1.75
            },
            "rcRadio": {
                'type': 'sbus',
                'calibrationStatus': False,
                "num_channels": 4,
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
