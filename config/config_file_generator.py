"""
airPy is a flight controller based on pyboard and written in micropython.

The MIT License (MIT)
Copyright (c) 2016 Fabrizio Scimia, fabrizio.scimia@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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
