# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb
from util.airpy_config_utils import save_config_file, load_config_file


#pyb.main('test_i2c.py') # main script to run after this one
#pyb.main('irqtest.py') # main script to run after this one
pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

config = load_config_file("app_config.json")
config['serial_only'] = False

pyb.LED(3).on()                 # indicate we are waiting for switch press
pyb.delay(2000)                 # wait for user to maybe press the switch
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
