
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Mar 20 23:32:24 2016

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
        self.tmp_pulse_width = None
        self.tmp_thrust = None
        self.tmp_pid = None

        # Motors
        self._num_motors = self.config_manager.get_param('num_motors')
        self._motors = [pyb.Servo(index) for index in range(1, self._num_motors+1)]

        # ESC
        self._esc_pwm_min_cmd = self.config_manager.get_param_set('esc', 'esc_pwm_min_cmd')
        self._esc_pwm_center = self.config_manager.get_param_set('esc', 'esc_pwm_center')
        self._esc_pwm_min = self.config_manager.get_param_set('esc', 'esc_pwm_min')
        self._esc_pwm_max = self.config_manager.get_param_set('esc', 'esc_pwm_max')
        self._esc_low_range = self._esc_pwm_center - self._esc_pwm_min
        self._esc_high_range = self._esc_pwm_max - self._esc_pwm_center

        # Set the esc pwm range in the attitude ctrl. it is not elegant but saves avoid calculating it each time at
        # pwm rate
        self.attitude_controller.set_esc_range(self._esc_pwm_max - self._esc_pwm_min)

        # TODO: handling of missing calibration

        self.throttle_min = self.config_manager.get_param_set('rcRadio', 'channels_default_min')[0]
        self.throttle_max = self.config_manager.get_param_set('rcRadio', 'channels_default_max')[0]
        self.throttle_center = self.config_manager.get_param_set('rcRadio', 'channels_default_center')[0]
        self.throttle_low_range = self.throttle_center - self.throttle_min
        self.throttle_high_range = self.throttle_max - self.throttle_center

        # Test
        # for k in range(180,1800,20):
        #    logger.debug("input: {} -> Output:{}".format(k, self.get_pwm_from_range(k)))

        # Motor Range Calibration
        for i in range(0, self._num_motors):
            self._motors[i].calibration(self._esc_pwm_min_cmd, self._esc_pwm_max, self._esc_pwm_center)

        logger.info("Throttle MIN/MAX/MID: {}/{}/{}".format(self.throttle_min, self.throttle_max, self.throttle_center))
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
            self.tmp_pwm = int(round(self._esc_pwm_center + ((pulse_width - self.throttle_center) / self.throttle_high_range) * self._esc_high_range))
        return self.tmp_pwm

    def set_thrust_passthrough(self):
        # set the thrust of all the motors without attitude contribution
        for j in range(0, self._num_motors):
            self._motors[j].pulse_width(self.get_pwm_from_range(self.rc_control.get_channel(1)))

    def set_zero_thrust(self):
        # set the thrust of all the motors to 0. Used for esc setup
        for j in range(0, self._num_motors):
            self._motors[j].pulse_width(self._esc_pwm_min)

    def set_thrust(self):
        # set the thrust of all the motors without attitude contribution TODO: generalize for more than 4 motors
        self.tmp_thrust = self.get_pwm_from_range(self.rc_control.get_channel(1))
        self.tmp_pid = self.attitude_controller.get_pid_increment()

        for j in range(0, self._num_motors):
            if j == 0:
                # motor front right
                self.tmp_pulse_width = self.tmp_thrust + self.tmp_pid
                if self.tmp_pulse_width < self._esc_pwm_min:
                    self._motors[j].pulse_width(self._esc_pwm_min)
                elif self.tmp_pulse_width > self._esc_pwm_max:
                    self._motors[j].pulse_width(self._esc_pwm_max)
                else:
                    self._motors[j].pulse_width(self.tmp_pulse_width)

            elif j == 1:
                # motor rear left
                self.tmp_pulse_width = self.tmp_thrust - self.tmp_pid
                if self.tmp_pulse_width < self._esc_pwm_min:
                    self._motors[j].pulse_width(self._esc_pwm_min)
                elif self.tmp_pulse_width > self._esc_pwm_max:
                    self._motors[j].pulse_width(self._esc_pwm_max)
                else:
                    self._motors[j].pulse_width(self.tmp_pulse_width)

            elif j == 2:
                # motor front left
                self.tmp_pulse_width = self.tmp_thrust + self.tmp_pid
                if self.tmp_pulse_width < self._esc_pwm_min:
                    self._motors[j].pulse_width(self._esc_pwm_min)
                elif self.tmp_pulse_width > self._esc_pwm_max:
                    self._motors[j].pulse_width(self._esc_pwm_max)
                else:
                    self._motors[j].pulse_width(self.tmp_pulse_width)

            elif j == 3:
                # motor rear right
                self.tmp_pulse_width = self.tmp_thrust - self.tmp_pid
                if self.tmp_pulse_width < self._esc_pwm_min:
                    self._motors[j].pulse_width(self._esc_pwm_min)
                elif self.tmp_pulse_width > self._esc_pwm_max:
                    self._motors[j].pulse_width(self._esc_pwm_max)
                else:
                    self._motors[j].pulse_width(self.tmp_pulse_width)