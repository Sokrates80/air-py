# -*- coding: utf-8 -*-
"""
AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

13-Dec-2015 Initial Release
20-Jan-2016 Refactor to be compliant with PEP8

"""

# import sys
from imu.mpu9150 import MPU9150
from fusion.fusion import Fusion
from attitude.pid_controller import PIDController
import util.airpy_logger as logger


class AttitudeController:
    def __init__(self, config_m, imu_update_freq):
        self.rc_control = None
        self.config_manager = config_m
        self._sampling_time = 1/imu_update_freq  # seconds

        # IMU
        self.imu = MPU9150('X')
        self.state = Fusion()

        # PID Controller
        self._max_increment = self.config_manager.get_param_set('attitude', 'max_increment')
        self._max_pitch = self.config_manager.get_param_set('attitude', 'max_pitch')
        self._max_roll = self.config_manager.get_param_set('attitude', 'max_roll')
        self._Kp = self.config_manager.get_param_set('attitude', 'Kp')
        self._Kd = self.config_manager.get_param_set('attitude', 'Kd')
        self._Ki = self.config_manager.get_param_set('attitude', 'Ki')
        self.pid_controller_pitch = PIDController()
        self.pid_controller_pitch.set_tunings(self._Kp, self._Kd, self._Ki, self._sampling_time, -1, 1)
        self.pid_controller_roll = PIDController()
        self.pid_controller_roll.set_tunings(self._Kp, self._Kd, self._Ki, self._sampling_time, -1, 1)
        self.pid_pitch_value = 0
        self.pid_roll_value = 0
        self._esc_range = 0

        # self.p_desired = 0  # hovering
        # self.q_desired = 0  # hovering
        # self.r_des = 0
        # self.phi_desired = 0  # hovering
        # self.theta_desired = 0  # hovering

        logger.info("AttitudeController Started")

    def set_rc_controller(self, rc_ctrl):
        self.rc_control = rc_ctrl

    def set_esc_range(self, esc_range):
        self._esc_range = esc_range*self._max_increment

    def get_rc_controller(self):
        return self.rc_control

    def update_state(self):
        self.state.update(self.imu.accel.xyz, self.imu.gyro.xyz, self.imu.mag.xyz)

        # TODO: desired state = 0 is only for hoovering
        self.pid_pitch_value = int(self.pid_controller_pitch.get_pid(self.state.pitch/self._max_pitch, 0)*self._esc_range)
        self.pid_roll_value = int(self.pid_controller_roll.get_pid(self.state.roll/self._max_roll, 0)*self._esc_range)
        # logger.debug("{};{}".format(self.state.pitch, self.pid_pitch_value))

    def get_attitude_status(self):
        return [self.state.pitch, self.state.roll, self.state.heading]

    def get_pid_increment(self):
        return [self.pid_pitch_value, self.pid_roll_value]


