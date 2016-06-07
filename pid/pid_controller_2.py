"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Apr 10 23:32:24 2016

@author: Fabrizio Scimia


"""


class PIDController:

    def __init__(self, p=0, i=0, d=0, imax=0):
        # settings
        self._Kp = float(p)
        self._Kd = float(d)
        self._Ki = float(i)
        self._min_output = imax
        self._max_output = -imax
        self.last_current_state = 0
        self.derivative_input = 0
        self.i_term = 0
        self.error = 0
        self.derivative_error = 0
        self.output = 0

    def get_pid(self, current_state, desired_state, scaler=1):

        # Current Error
        self.error = desired_state - current_state

        # Integral of the error
        self.i_term += self._Ki*self.error

        if self.i_term > self._max_output:
            self.i_term = self._max_output
        elif self.i_term < self._min_output:
            self.i_term = self._min_output

        # Derivative error
        self.derivative_input = current_state - self.last_current_state
        self.last_current_state = current_state

        self.output = self._Kp*self.error + self.i_term - self._Kd*self.derivative_input

        if self.output > self._max_output:
            self.output = self._max_output
        elif self.output < self._min_output:
            self.output = self._min_output

        return self.output

    def update_pid_settings(self, kp, ki, kd, max_output, delta_t):
        self._Kp = kp
        self._Kd = float(kd) / float(delta_t)
        self._Ki = ki * delta_t
        self._min_output = -max_output
        self._max_output = max_output
        self.reset_I()

    def reset_I(self):
        self.i_term = 0
        self.last_current_state = 0

