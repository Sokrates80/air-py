"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Mar 20 23:32:24 2016

@author: Fabrizio Scimia


"""


class PIDController:
    def __init__(self):
        # settings
        self._Kp = 0
        self._Kd = 0
        self._Ki = 0
        self._min_output = 0
        self._max_output = 0

        # working vars
        self.last_error = 0
        self.i_term = 0
        self.error = 0
        self.derivative_error = 0
        self.output = 0

    def get_pid(self, current_state, desired_state):
        self.error = desired_state - current_state
        self.i_term += self._Ki*self.error

        if self.i_term > self._max_output:
            self.i_term = self._max_output
        elif self.i_term < self._min_output:
            self.i_term = self._min_output

        self.derivative_error = (self.error - self.last_error)
        self.last_error = self.error

        self.output = self._Kp*self.error + self.i_term + self._Kd*self.derivative_error

        if self.output > self._max_output:
            self.output = self._max_output
        elif self.output < self._min_output:
            self.output = self._min_output

        return self.output

    def set_tunings(self, kp, kd, ki, delta_t, min_output, max_output):
        self._Kp = kp
        self._Kd = kd / delta_t
        self._Ki = ki * delta_t
        self._min_output = min_output
        self._max_output = max_output
