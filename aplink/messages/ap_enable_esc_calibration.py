"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

"""
from util.airpy_config_utils import save_config_file, load_config_file


class EnableEscCalibration:

    MESSAGE_TYPE_ID = 60

    def __init__(self):
        pass

    @staticmethod
    def enable_esc_calibration():
        '''
        Used to enable esc calibration by changing a flag in the app_config.json. By rebooting the board the change
        will take effect. Rebooting the board again the standard mode will be restored.
        :return:
        '''
        config = load_config_file("app_config.json")
        config['esc_calibration_mode'] = True
        save_config_file("app_config.json", config)