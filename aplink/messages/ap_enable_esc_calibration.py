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
from util.airpy_config_utils import save_config_file, load_config_file


class EnableEscCalibration:

    MESSAGE_TYPE_ID = 60

    def __init__(self):
        pass

    @staticmethod
    def enable_esc_calibration():
        '''
        Used to enable esc calibration by changing a flag in the app_config.json. By rebooting the board the change
        will take effect. Rebooting the board again the standard mode will be restored.
        :return:
        '''
        config = load_config_file("app_config.json")
        config['esc_calibration_mode'] = True
        save_config_file("app_config.json", config)