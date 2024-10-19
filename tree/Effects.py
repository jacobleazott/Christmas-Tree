# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    <NAME>                        CREATED: YYYY-MM-DD          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# 
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import logging
import multiprocessing
import os
import signal
import sys
import time


from rpi_ws281x import PixelStrip, Color

from coords import coordinates
from Settings import Settings
from decorators import *

from Led_Controller import LEDController
import Color_Helpers as CH
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDEffects():
    
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        
        self.pixel_data = [None] * (Settings.NUM_LEDS + 5)
        
        self.min_and_max = (self.find_min_max(0), self.find_min_max(1), self.find_min_max(2))
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def find_min_max(self, axis):
        min_val = sys.maxsize
        max_val = -sys.maxsize - 1
        for elem in coordinates:
            min_val = min(min_val, elem[axis])
            max_val = max(max_val, elem[axis])
        return min_val, max_val
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def rainbow(self, axis, step, width):
        
        height = self.min_and_max[axis][1] - self.min_and_max[axis][0]
        height_hue_step = 2 * width * ( 360 / height )
        
        count = 0
        with LEDController(refresh_rate_hz=35, logger=self.logger) as led_controller:
            while True:
                for i in range( 0, int(height / (2 * width)), int(height * step) ):
                    for pixel in range( Settings.NUM_LEDS ):
                        val = (abs(coordinates[pixel][axis] - i ) * height_hue_step) % 360
                        self.pixel_data[pixel] = CH.hue_to_rgb_corrected(val)
                    count += 1
                    self.pixel_data[Settings.NUM_LEDS+1] = count
                    led_controller.update_leds(self.pixel_data)


if __name__ == "__main__":
    effect = LEDEffects()
    effect.rainbow(0, 0.01, 0.75)


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════



    

