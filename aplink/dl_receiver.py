"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sat Mar 12 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

12-Mar-2016 Initial Release

"""


class DLReceiver:
    def __init__(self, streamer):
        self.byte_streamer = streamer
