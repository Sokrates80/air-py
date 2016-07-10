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

# boot.py -- run on boot-up

# import machine
import pyb
from utils.airpy_config_utils import save_config_file, load_config_file

config = load_config_file("app_config.json")
config['serial_only'] = False

boot_delay = 2000

if config['esc_calibration_mode']:  # if esc calibration is true set esc_calibration script to run after this one
    pyb.main('./attitude/esc_calibration.py')
    config['esc_calibration_mode'] = False
    boot_delay = 0  # avoid the boot delay to proceed with esc calibration
else:
    pyb.main('main.py')  # if esc calibration is false set main script to run after this one
    # pyb.main('./aplink/test/test_ap_save_tx_settings.py')  # TEST

pyb.LED(3).on()                 # indicate we are waiting for switch press
pyb.delay(boot_delay)           # wait for user to maybe press the switch
switch_value = pyb.Switch()()   # sample the switch at end of delay
pyb.LED(3).off()                # indicate that we finished waiting for the switch

pyb.LED(4).on()                 # indicate that we are selecting the mode

if switch_value:
    pyb.usb_mode('CDC+MSC')
else:
    pyb.usb_mode('CDC+HID')
    config['serial_only'] = True

save_config_file("app_config.json", config)

pyb.LED(4).off()                # indicate that we finished selecting the mode
