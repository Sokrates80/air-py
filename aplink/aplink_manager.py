"""

AirPy - MicroPython based autopilot v. 0.0.1

Created on Sun Dec 13 23:32:24 2015

@author: Fabrizio Scimia

Revision History:

20-Jan-2016 Initial Release

"""


from aplink.ul_mux import ULMux


class APLinkManager:
    def __init__(self):
        self.UL = ULMux()
