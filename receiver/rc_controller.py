
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

import pyb
import array
import util.airpy_logger as logger
from receiver.sbus_receiver import SBUSReceiver


class RCController:
    def __init__(self, config_m):
        """
        This class is used as interface to handle different type of RC receivers. At the moment Frsky SBUS is the only
         one tested and supported (X8R, X6R, X4R)
        :param config_m: and object ConfigFileManager used to retrieve RC configuration parameters
        """
        # TODO select dynamically the receiver type
        self.rcCtrl = SBUSReceiver()
        self.report = ''
        self.start_timer = 0
        self.time_count = 0
        self._IDLE = 0
        self._ARMED = 1
        self.channels_ratio = array.array('f', [0, 0, 0, 0])
        self.channels = None
        self.mapped_value = None

        # load rc specific parameters (they should come from airPyGS RC Calibration) TODO: check if calibrated
        self.num_channels = config_m.get_param_set('rcRadio', 'num_channels')
        self.channels_min = config_m.get_param_set('rcRadio', 'channels_min')
        self.channels_max = config_m.get_param_set('rcRadio', 'channels_max')
        self.channels_center = config_m.get_param_set('rcRadio', 'channels_center')
        self.channels_low_range = list(map(lambda m, n: m-n, self.channels_center, self.channels_min))
        self.channels_high_range = list(map(lambda m, n: m-n, self.channels_max, self.channels_center))
        self.channels_full_range = list(map(lambda m, n: m-n, self.channels_max, self.channels_min))

        # TODO: include in settings file and in GUI calibration
        self.thrust_ch_index = 0
        self.yaw_ch_index = 3
        self.pitch_ch_index = 2
        self.roll_ch_index = 1

        logger.info("RCController Started")

    def update_rx_data(self):
        self.rcCtrl.get_new_data()

    def map_range(self, ch_value, ch_index):

        if ch_value > self.channels_center[ch_index]:
            self.mapped_value = (ch_value - self.channels_center[ch_index])/self.channels_high_range[ch_index]
        else:
            self.mapped_value = (ch_value - self.channels_center[ch_index])/self.channels_low_range[ch_index]

        return self.mapped_value

    def update_channels_ratio(self):
        """
        Used to retrieve the PWM channels values from the RC receiver and translate them into percentage values.
        """
        self.channels = self.rcCtrl.get_rx_channels()
        self.channels_ratio[0] = self.channels[self.thrust_ch_index]/self.channels_full_range[self.thrust_ch_index]
        self.channels_ratio[1] = self.map_range(self.channels[self.yaw_ch_index], self.yaw_ch_index)
        self.channels_ratio[2] = self.map_range(self.channels[self.pitch_ch_index], self.pitch_ch_index)
        self.channels_ratio[3] = self.map_range(self.channels[self.roll_ch_index], self.roll_ch_index)

    def check_arming(self):
        check = False
        if self.get_channel(1) < 250 and self.get_channel(3) < 250 and self.get_channel(4) > 1600:
            if self.start_timer > 0:
                if pyb.elapsed_millis(self.start_timer) > 3000:  # 3 sec
                    check = True
                    self.start_timer = 0
            else:
                self.start_timer = pyb.millis()
        else:
            self.start_timer = 0

        return check

    def get_channels_ratio(self):
        """
        Used to retrieve all channels ratio value at once.
        :return: an array containing the ratio value for all the 4 channels
        """
        self.update_channels_ratio()
        return self.channels_ratio

    def check_idle(self):
        check = False
        if self.get_channel(1) < 250:
            if self.start_timer > 0:
                if pyb.elapsed_millis(self.start_timer) > 5000:  # 5 sec
                    check = True
                    self.start_timer = 0
            else:
                self.start_timer = pyb.millis()
        else:
            self.start_timer = 0

        return check

    def get_report(self):
        self.report = self.rcCtrl.get_rx_report()
        return self.report

    def get_channels(self):
        return self.rcCtrl.get_rx_channels()

    def get_channel(self, num_channel):
        return self.rcCtrl.get_rx_channel(num_channel - 1)  # convert from 0->n to 1->(n+1)

    def get_link_status(self):
        return self.rcCtrl.get_failsafe_status()
