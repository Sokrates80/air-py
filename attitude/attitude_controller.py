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

# import sys
import util.airpy_logger as logger
from fusion.fusion import Fusion
from imu.mpu9150 import MPU9150
from pid.pid import PID
import array


class AttitudeController:
    def __init__(self, config_m, imu_update_freq, rc_ctrl, esc_ctrl):
        self.rc_control = rc_ctrl
        self._sampling_time = float(1.0/imu_update_freq)  # seconds

        # State Definition
        self.IDLE = 0
        self.ARMED = 1
        self.FAIL_SAFE = 2

        # IMU
        self.imu = MPU9150('X')
        self.imu.filter_range = 2
        self.state = Fusion()
        self.gyros = []

        # ESC
        self.esc_controller = esc_ctrl
        self.tmp_pulse_width = array.array('H', [0, 0, 0, 0])  # TODO: initialize based on # of motors

        # PID Controller
        self.channels_rate = array.array('f', [0, 0, 0, 0])
        self._max_increment = config_m.get_param_set('attitude', 'max_increment')
        self._max_gyro_increment = config_m.get_param_set('attitude', 'max_gyro_increment')
        self._max_pitch = -(config_m.get_param_set('attitude', 'max_pitch'))
        self._max_roll = -(config_m.get_param_set('attitude', 'max_roll'))
        self._max_yaw = -(config_m.get_param_set('attitude', 'max_yaw'))
        self._stab_Kp = config_m.get_param_set('attitude', 'stab_Kp')
        self._stab_Kd = config_m.get_param_set('attitude', 'stab_Kd')
        self._stab_Ki = config_m.get_param_set('attitude', 'stab_Ki')
        self._gyro_Kp = config_m.get_param_set('attitude', 'gyro_Kp')
        self._gyro_Kd = config_m.get_param_set('attitude', 'gyro_Kd')
        self._gyro_Ki = config_m.get_param_set('attitude', 'gyro_Ki')
        self._pitch_offset = config_m.get_param_set('attitude', 'pitch_offset')
        self._pitch_rate_offset = config_m.get_param_set('attitude', 'pitch_rate_offset')
        self._roll_offset = config_m.get_param_set('attitude', 'roll_offset')
        self._roll_rate_offset = config_m.get_param_set('attitude', 'roll_rate_offset')
        self.pitch_correct_angle = 0
        self.roll_correct_angle = 0
        self.yaw_correct_ang_vel = 0

        # Initialize PIDs
        self.pid_controller_pitch = PID(p=self._stab_Kp, i=self._stab_Ki, d=self._stab_Kd, imax=self._max_increment)
        self.pid_controller_rate_pitch = PID(p=self._gyro_Kp, i=self._gyro_Ki, d=self._gyro_Kd, imax=self._max_gyro_increment)
        self.pid_controller_roll = PID(p=self._stab_Kp, i=self._stab_Ki, d=self._stab_Kd, imax=self._max_increment)
        self.pid_controller_rate_roll = PID(p=self._gyro_Kp, i=self._gyro_Ki, d=self._gyro_Kd, imax=self._max_gyro_increment)
        self.pid_controller_rate_yaw = PID(p=self._gyro_Kp, i=self._gyro_Ki, d=self._gyro_Kd, imax=self._max_gyro_increment)
        self.pitch_stab_out = 0
        self.roll_stab_out = 0
        self.pitch_out = 0
        self.roll_out = 0
        self.yaw_out = 0

        logger.info("AttitudeController Started - IMU Sampling Time = {}".format(self._sampling_time))
        logger.info("Stabilization PIDs:{}/{}/{}".format(self._stab_Kp, self._stab_Ki, self._stab_Kd))
        logger.info("Gyro PIDs:{}/{}/{}".format(self._gyro_Kp, self._gyro_Ki, self._gyro_Kd))

    def get_rc_controller(self):
        return self.rc_control

    def set_PID_settings(self, pids):
        self._stab_Kp = pids[0]
        self._stab_Kd = pids[1]
        self._stab_Ki = pids[2]
        self._max_increment = pids[3]
        self._gyro_Kp = pids[4]
        self._gyro_Kd = pids[5]
        self._gyro_Ki = pids[6]
        self._max_gyro_increment = pids[7]

        # update angle pids settings in all active pid objects
        self.pid_controller_pitch.update_pid_settings(self._stab_Kp, self._stab_Ki, self._stab_Kd, self._max_increment)
        self.pid_controller_roll.update_pid_settings(self._stab_Kp, self._stab_Ki, self._stab_Kd, self._max_increment)
        # rate pids
        self.pid_controller_rate_pitch.update_pid_settings(self._gyro_Kp, self._gyro_Ki, self._gyro_Kd, self._max_gyro_increment)
        self.pid_controller_rate_roll.update_pid_settings(self._gyro_Kp, self._gyro_Ki, self._gyro_Kd, self._max_gyro_increment)
        self.pid_controller_rate_yaw.update_pid_settings(self._gyro_Kp, self._gyro_Ki, self._gyro_Kd, self._max_gyro_increment)

    def get_pid_settings(self):
        return [self._stab_Kp, self._stab_Kd, self._stab_Ki, self._max_increment,
                self._gyro_Kp, self._gyro_Kd, self._gyro_Ki, self._max_gyro_increment]

    # TODO: this is not working. Fix it!
    def gyro_calibration(self, enable):
        self.imu.gyro_calibration(enable)

    def update_state(self):
        # saving gyros for sending through telemetry
        self.gyros = self.imu.gyro.xyz
        # self.state.update_nomag(self.imu.accel.xyz, self.gyros)
        self.state.update(self.imu.accel.xyz, self.gyros, self.imu.mag_nonblocking.xyz)

    def get_attitude_status(self):
        # return [self.state.pitch, self.state.roll, self.state.heading]
        return [self.state.pitch+self._pitch_offset, self.state.roll+self._roll_offset, self.state.heading,
                self.gyros[1]+self._pitch_rate_offset, self.gyros[0]+self._roll_rate_offset, self.gyros[2]]

    def get_pulse_widths(self):
        return self.esc_controller.pulse_widths

    def update_esc(self, state):

        if state == self.ARMED:

            # PID calculation
            self.channels_rate = self.rc_control.get_channels_ratio()
            self.tmp_pulse_width = [self.esc_controller.esc_pwm_min
                                    + int(self.esc_controller.esc_full_range*self.channels_rate[0]), 0, 0, 0]

            if self.channels_rate[0] > 0.2:

                    # stabilize pid calculation
                    self.pitch_stab_out = max(min(self.pid_controller_pitch.get_pid(
                                                                             -(self.state.pitch + self._pitch_offset),
                                                                            -self.channels_rate[2] * self._max_pitch, 1
                                                  ), 250), -250)
                    self.roll_stab_out = max(min(self.pid_controller_roll.get_pid(-(self.state.roll + self._roll_offset),
                                                                                  -self.channels_rate[3] * self._max_roll
                                                                                  , 1), 250), -250)

                    # rate pid calculation
                    self.pitch_out = max(min(self.pid_controller_rate_pitch.get_pid(-(self.gyros[1] + self._pitch_rate_offset),
                                                                                    self.pitch_stab_out,
                                                                               1), 500), -500)

                    self.roll_out = max(min(self.pid_controller_rate_roll.get_pid(-(self.gyros[0] + self._roll_rate_offset),
                                                                                  self.roll_stab_out,
                                                                                1), 500), -500)

                    self.yaw_out = max(min(self.pid_controller_rate_yaw.get_pid(self.gyros[2],
                                                                                self.channels_rate[1] * self._max_yaw, 1), 500), -500)

                    # To avoid correction for very slow drift
                    if abs(self.channels_rate[1] * self._max_yaw - self.gyros[2]) < 3:
                        self.yaw_out = 0
                        self.pid_controller_rate_yaw.reset_I()

                    # calculate PID increment
                    self.tmp_pulse_width[1] = int(self.pitch_out)
                    self.tmp_pulse_width[2] = int(self.roll_out)
                    self.tmp_pulse_width[3] = int(self.yaw_out)

            else:
                    self.pid_controller_pitch.reset_I()
                    self.pid_controller_rate_pitch.reset_I()
                    self.pid_controller_roll.reset_I()
                    self.pid_controller_rate_roll.reset_I()
                    self.pid_controller_rate_yaw.reset_I()

            # Update motor thrusts
            self.esc_controller.set_thrust(self.tmp_pulse_width)

        elif state == self.IDLE:

            self.esc_controller.set_zero_thrust()

