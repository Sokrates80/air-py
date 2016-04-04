# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb
from util.airpy_config_utils import save_config_file, load_config_file

config = load_config_file("app_config.json")
config['serial_only'] = False

boot_delay = 2000

if config['esc_calibration_mode']:  # if esc calibration is true set esc_calibration script to run after this one
    pyb.main('./attitude/esc_calibration.py')
    config['esc_calibration_mode'] = False
    boot_delay = 0  # avoid the boot delay to proceed with esc calibration
else:
    pyb.main('main.py')  # if esc calibration is false set main script to run after this one

pyb.LED(3).on()                 # indicate we are waiting for switch press
pyb.delay(boot_delay)                 # wait for user to maybe press the switch
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