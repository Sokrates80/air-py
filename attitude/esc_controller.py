
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
        self.tmp_thrust = None
        self.tmp_pid_pitch = None
        self.tmp_pid_roll = None

        # ESC parameters
        self._esc_pwm_min_cmd = self.config_manager.get_param_set('esc', 'esc_pwm_min_cmd')
        self._esc_pwm_center = self.config_manager.get_param_set('esc', 'esc_pwm_center')
        self._esc_pwm_min = self.config_manager.get_param_set('esc', 'esc_pwm_min')
        self._esc_pwm_max = self.config_manager.get_param_set('esc', 'esc_pwm_max')
        self._esc_low_range = self._esc_pwm_center - self._esc_pwm_min
        self._esc_high_range = self._esc_pwm_max - self._esc_pwm_center
        # Threshold at 10% for the PID start working
        self._esc_pid_threshold = abs(0.1*(self._esc_pwm_max - self._esc_pwm_min)) + self._esc_pwm_min

        # Set the esc pwm range in the attitude ctrl. it is not elegant but saves avoid calculating it each time at
        # pwm rate
        self.attitude_controller.set_esc_range(self._esc_pwm_max - self._esc_pwm_min)

        # RADIO parameters TODO: handling of missing calibration
        self.throttle_min = self.config_manager.get_param_set('rcRadio', 'channels_default_min')[0]
        self.throttle_max = self.config_manager.get_param_set('rcRadio', 'channels_default_max')[0]
        self.throttle_center = self.config_manager.get_param_set('rcRadio', 'channels_default_center')[0]
        self.throttle_low_range = self.throttle_center - self.throttle_min
        self.throttle_high_range = self.throttle_max - self.throttle_center

        # PWM initialization TODO: hexacopter handling
        self._num_motors = self.config_manager.get_param('num_motors')

        self.tmp_pulse_width = [0 for x in range(0, self._num_motors)]

        # set PWM to 400Hz TODO: set freq according to settings
        self._timers = [Timer(self.config_manager.get_param_set('esc', 'quadcopter')['timers'][index],
                              prescaler=83, period=2499) for index in range(0, self._num_motors)]

        self._escs = [self._timers[index].channel(self.config_manager.get_param_set('esc',
                                                                                    'quadcopter')['channels'][index],
                                                  Timer.PWM,
                                                  pin=Pin(self.config_manager.get_param_set('esc',
                                                                                            'quadcopter')['pins'][index]
                                                          )
                                                  ) for index in range(0, self._num_motors)]
        # TODO: hexacopter handling
        self._front_esc_indexes = [0, 2]
        self._rear_esc_indexes = [1, 3]
        self._left_esc_indexes = [1, 2]
        self._right_esc_indexes = [0, 3]

        logger.info("Esc Controller Started")

    def get_pwm_from_range(self, pulse_width):
        """
        Used to convert the Rc pulse width dynamic to the ESC specific dynamic
        :param pulse_width: pulse width value from Rc Receiver
        :return: normalized value according with ESC dynamic
        """
        if pulse_width <= self.throttle_center:
            self.tmp_pwm = self._esc_pwm_min_cmd + int((pulse_width/self.throttle_low_range)*self._esc_low_range)
        else:
            self.tmp_pwm = int(self._esc_pwm_center +
                               ((pulse_width - self.throttle_center) / self.throttle_high_range) * self._esc_high_range)
        return self.tmp_pwm

    def set_thrust_passthrough(self):

        # set the thrust of all the motors without attitude contribution
        self.tmp_thrust = self.get_pwm_from_range(self.rc_control.get_channel(1))
        # print(self.tmp_thrust)
        for j in range(0, self._num_motors):
            self._escs[j].pulse_width(self.tmp_thrust)

    def set_zero_thrust(self):
        # set the thrust of all the motors to 0. Used for esc setup
        for j in range(0, self._num_motors):
            self._escs[j].pulse_width(self._esc_pwm_min_cmd)

    def set_thrust(self):
        self.tmp_thrust = self.get_pwm_from_range(self.rc_control.get_channel(1))
        if self.tmp_thrust > self._esc_pid_threshold:
            self.tmp_pid_pitch = self.attitude_controller.get_pid_increment()[0]
            self.tmp_pid_roll = self.attitude_controller.get_pid_increment()[1]
            # DEBUG PID
            # logger.debug("{};{};{}".format(self.tmp_thrust, self.tmp_pid_pitch, self.tmp_pid_roll))
            # TODO: Generalize for quad and hex
            self._escs[0].pulse_width(min(max(self._esc_pwm_min, self.tmp_thrust + self.tmp_pid_pitch + self.tmp_pid_roll),
                                          self._esc_pwm_max))
            self._escs[1].pulse_width(min(max(self._esc_pwm_min, self.tmp_thrust - self.tmp_pid_pitch - self.tmp_pid_roll),
                                          self._esc_pwm_max))
            self._escs[2].pulse_width(min(max(self._esc_pwm_min, self.tmp_thrust + self.tmp_pid_pitch - self.tmp_pid_roll),
                                          self._esc_pwm_max))
            self._escs[3].pulse_width(min(max(self._esc_pwm_min, self.tmp_thrust - self.tmp_pid_pitch + self.tmp_pid_roll),
                                          self._esc_pwm_max))
        else:
            self.set_thrust_passthrough()

        # logger.debug('Trust:{}, Pitch_PID:{}, list:{}'.format(self.tmp_thrust, self.tmp_pid_pitch, self.tmp_pulse_width))






