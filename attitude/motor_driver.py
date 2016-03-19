
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

"""

# import sys
import pyb
import util.airpy_logger as logger


class MotorDriver:
    def __init__(self, config_m, attitude_ctrl):
        self.attitude_controller = attitude_ctrl
        self.rc_control = attitude_ctrl.get_rc_controller()
        self.config_manager = config_m
        self.tmp_pwm = None

        # Motors
        self._num_motors = self.config_manager.get_param('num_motors')
        self._motors = [pyb.Servo(index) for index in range(1, self._num_motors+1)]

        # ESC
        self._esc_pwm_min_cmd = self.config_manager.get_param_set('rcRadio', 'esc_pwm_min_cmd')
        self._esc_pwm_min_center = self.config_manager.get_param_set('rcRadio', 'esc_pwm_min_center')
        self._esc_pwm_min = self.config_manager.get_param_set('rcRadio', 'esc_pwm_min')
        self._esc_pwm_max = self.config_manager.get_param_set('rcRadio', 'esc_pwm_max')
        self._esc_low_range = self._esc_pwm_min_center - self._esc_pwm_min
        self._esc_high_range = self._esc_pwm_max - self._esc_pwm_min_center

        # TODO: handling of missing calibration

        self.throttle_min = self.config_manager.get_param_set('rcRadio', 'channels_default_min')[0]
        self.throttle_max = self.config_manager.get_param_set('rcRadio', 'channels_default_max')[0]
        self.throttle_center = self.config_manager.get_param_set('rcRadio', 'channels_default_center')[0]
        self.throttle_low_range = self.throttle_center - self.throttle_min
        self.throttle_high_range = self.throttle_max - self.throttle_center
        logger.info("Throttle MIN/MAX/MID: {}/{}/{}".format(self.throttle_min, self.throttle_max, self.throttle_center))

        # Test
        # for k in range(180,1800,20):
        #    logger.debug("input: {} -> Output:{}".format(k, self.get_pwm_from_range(k)))

        # Motor Range Calibration
        for i in range(0, self._num_motors):
            self._motors[i].calibration(self._esc_pwm_min_cmd, self._esc_pwm_max, self._esc_pwm_min_center)

        logger.info("Motor Driver Started")

    def get_pwm_from_range(self, pulse_width):
        """
        Used to convert the Rc pulse width dynamic to the ESC specific dynamic
        :param pulse_width: pulse width value from Rc Receiver
        :return: normalized value according with ESC dynamic
        """
        if pulse_width <= self.throttle_center:
            self.tmp_pwm = self._esc_pwm_min_cmd + int(round((pulse_width/self.throttle_low_range)*self._esc_low_range))
        else:
            self.tmp_pwm = int(round(self._esc_pwm_min_center + ((pulse_width-self.throttle_center)/self.throttle_high_range)*self._esc_high_range))
        return self.tmp_pwm

    def set_thrust_passthrough(self):
        # set the thrust of all the motors without attitude contribution
        for j in range(0, self._num_motors):
            self._motors[j].pulse_width(self.get_pwm_from_range(self.rc_control.get_channel(1)))