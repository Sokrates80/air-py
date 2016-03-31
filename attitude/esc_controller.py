
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Mar 30 23:32:24 2016

@author: Fabrizio Scimia

"""

from pyb import Pin, Timer
import util.airpy_logger as logger


class EscController:

    def __init__(self, config_m, attitude_ctrl, pwm_rate):

        self.attitude_controller = attitude_ctrl
        self.rc_control = attitude_ctrl.get_rc_controller()
        self.config_manager = config_m
        self._pwm_refresh_rate = pwm_rate
        self.tmp_pwm = None
        self.tmp_pulse_width = None
        self.tmp_thrust = None
        self.tmp_pid = None

        # ESC parameters
        self._esc_pwm_min_cmd = self.config_manager.get_param_set('esc', 'esc_pwm_min_cmd')
        self._esc_pwm_center = self.config_manager.get_param_set('esc', 'esc_pwm_center')
        self._esc_pwm_min = self.config_manager.get_param_set('esc', 'esc_pwm_min')
        self._esc_pwm_max = self.config_manager.get_param_set('esc', 'esc_pwm_max')
        self._esc_low_range = self._esc_pwm_center - self._esc_pwm_min
        self._esc_high_range = self._esc_pwm_max - self._esc_pwm_center

        # Set the esc pwm range in the attitude ctrl. it is not elegant but saves avoid calculating it each time at
        # pwm rate
        self.attitude_controller.set_esc_range(self._esc_pwm_max - self._esc_pwm_min)

        # RADIO parameters TODO: handling of missing calibration
        self.throttle_min = self.config_manager.get_param_set('rcRadio', 'channels_default_min')[0]
        self.throttle_max = self.config_manager.get_param_set('rcRadio', 'channels_default_max')[0]
        self.throttle_center = self.config_manager.get_param_set('rcRadio', 'channels_default_center')[0]
        self.throttle_low_range = self.throttle_center - self.throttle_min
        self.throttle_high_range = self.throttle_max - self.throttle_center

        # PWM initialization TODO: handle hexacopter
        self._num_motors = self.config_manager.get_param('num_motors')

        # DEBUG
        # for index in range(0, self._num_motors):
        #    logger.debug("esc{}:{}".format(index, self.config_manager.get_param_set('esc', 'quadcopter')['timers'][index]))

        # set PWM to 200Hz
        self._timers = [Timer(self.config_manager.get_param_set('esc', 'quadcopter')['timers'][index],
                              prescaler=83, period=4999) for index in range(0, self._num_motors)]
                              # freq=self._pwm_refresh_rate) for index in range(0, self._num_motors)]

        self._escs = [self._timers[index].channel(self.config_manager.get_param_set('esc', 'quadcopter')['channels'][index],
                                                  Timer.PWM,
                                                  pin=Pin(self.config_manager.get_param_set('esc', 'quadcopter')['pins'][index])
                                                  ) for index in range(0, self._num_motors)]

        logger.info("Esc Controller Started")

    def get_pwm_from_range(self, pulse_width):
        """
        Used to convert the Rc pulse width dynamic to the ESC specific dynamic
        :param pulse_width: pulse width value from Rc Receiver
        :return: normalized value according with ESC dynamic
        """
        if pulse_width <= self.throttle_center:
            self.tmp_pwm = self._esc_pwm_min_cmd + int(round((pulse_width/self.throttle_low_range)*self._esc_low_range))
        else:
            self.tmp_pwm = int(round(self._esc_pwm_center + ((pulse_width - self.throttle_center) / self.throttle_high_range) * self._esc_high_range))
        return self.tmp_pwm

    def set_thrust_passthrough(self):

        # set the thrust of all the motors without attitude contribution
        self.tmp_thrust = self.get_pwm_from_range(self.rc_control.get_channel(1))
        # print(self.tmp_thrust)
        for j in range(0, self._num_motors):
            self._escs[j].pulse_width(self.tmp_thrust)

    def set_zero_thrust(self):
        # set the thrust of all the motors to 0. Used for esc setup
        # print(self._esc_pwm_min)
        for j in range(0, self._num_motors):
            self._escs[j].pulse_width(self._esc_pwm_min_cmd)