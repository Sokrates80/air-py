from pid.test.pid_1 import PID

test_data = {
    1: [0, 0],
    2: [2, 0],
    3: [4, 10],
    4: [2, -5],
    5: [-20, -50],
    6: [-5, 10],
    7: [0, 5],
    8: [30, 20],
    9: [10, -10],
    10: [0, 0]
}

_stab_Kp = 4
_stab_Kd = 0.1
_stab_Ki = 1
_gyro_Kp = 0.7
_gyro_Kd = 0
_gyro_Ki = 1
_max_increment = 50
_max_gyro_increment = 50

pid1 = PID(p=_stab_Kp, i=_stab_Ki, d=_stab_Kd, imax=_max_increment)
pid2 = PID(p=_gyro_Kp, i=_gyro_Ki, d=_gyro_Kd, imax=_max_gyro_increment)
pid3 = PID(p=_stab_Kp, i=_stab_Ki, d=_stab_Kd, imax=_max_increment)
pid4 = PID(p=_gyro_Kp, i=_gyro_Ki, d=_gyro_Kd, imax=_max_gyro_increment)

for k, v in test_data.items():
    pid1_val = pid1.get_pid(v[0], 0, 1)
    pid2_val = pid2.get_pid(pid1_val, v[1], 1)
    pid3_val = pid3.get_pid(v[0], 0, 1)
    pid4_val = pid4.get_pid(pid3_val, v[1], 1)

    print("Result Pid 1 [{}; {}] -- Result Pid 2 [{}; {}]".format(pid1_val, pid2_val, pid3_val, pid4_val))