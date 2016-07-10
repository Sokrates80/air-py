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

import ustruct


class SavePIDSettings:

    MESSAGE_TYPE_ID = 70

    def __init__(self):
        pass

    @staticmethod
    def decode_payload(payload):
        """
        Decode message payload
        :param payload: byte stream representing the message payload
        :return: an array of 8 float [stab_Kp,stab_Kd,stab_Ki,Max Increment,gyro_Kp,gyro_Kd,gyro_Ki,gyro_Max Increment]
        """
        pid_settings = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for i in range(0, 8):
            pid_settings[i] = ustruct.unpack('>f', payload[i*4:i*4 + 4])[0]

        return pid_settings
