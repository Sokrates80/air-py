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
import util.airpy_logger as logger


class AttitudeController:
    def __init__(self, config_m):
        self.rc_control = None
        self.config_manager = config_m

        # IMU
        self.imu = MPU9150('X')
        self.state = Fusion()

        logger.info("AttitudeController Started")

    def set_rc_controller(self, rc_ctrl):
        self.rc_control = rc_ctrl

    def get_rc_controller(self):
        return self.rc_control

    def update_state(self):
        self.state.update(self.imu.accel.xyz, self.imu.gyro.xyz, self.imu.mag.xyz)

        # self.set_thrust(self.m1, self.rc_control.get_channel(1))
        # sys.stdout.write(str("Pitch: ") + str(self.state.pitch) + str(" - Roll: ") + str(self.state.roll)+ str(" - Yaw: ") + str(self.state.heading)+str('    \r'))
        # print("Pitch: ", self.state.pitch, " - Roll: ", self.state.roll, " - Yaw: ", self.state.heading)

    def get_attitude_status(self):
        return [self.state.pitch, self.state.roll, self.state.heading]

"""
p_des = 0;
q_des = 0;
r_des = des_state.yawdot;

k_p_phi*(phi_des-state.rot(1))+k_d_phi*(p_des-state.omega(1));
k_p_theta*(theta_des-state.rot(2))+k_d_theta*(q_des-state.omega(2));
k_p_psi*(des_state.yaw-state.rot(3))+k_d_psi*(r_des-state.omega(3));

"""


