# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    LED EFFECTS LIBRARY                      CREATED: 2024-10-19          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Collection of all of our LED Effects. If the effect is simple enough to be a single function it should just be added
#   on to this class. If it is more complex, it should be in its own file and imported here so we have all features
#   under this one class.
#
# Important note that the runner of our effects should never have to worry about LEDController, so any management of
#   that should be handled within this class as well.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import logging
import math
import random
import sys
import threading
import time


import numpy as np
import random
import colorsys

import helpers.Color_Helpers as CH
from helpers.decorators import *
from helpers.Settings import Settings
from coords import coordinates
from Led_Controller import LEDController        


def rotate_point(point, angles):
    # Convert angles from degrees to radians
    rx, ry, rz = np.radians(angles)

    # Rotation matrices
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(rx), -np.sin(rx)],
                    [0, np.sin(rx), np.cos(rx)]])
    
    R_y = np.array([[np.cos(ry), 0, np.sin(ry)],
                    [0, 1, 0],
                    [-np.sin(ry), 0, np.cos(ry)]])
    
    R_z = np.array([[np.cos(rz), -np.sin(rz), 0],
                    [np.sin(rz), np.cos(rz), 0],
                    [0, 0, 1]])

    # Combined rotation matrix
    R = R_z @ R_y @ R_x
    return R @ point


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Collection of LED effects and the handler of our LEDController.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDEffects(LogAllMethods):
    
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        
        self.pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        self.min_and_max = (self.find_min_max(0), self.find_min_max(1), self.find_min_max(2))
        
        self.led_controller = LEDController(refresh_rate_hz=35, logger=self.logger)
        
        self.run_effect = True
        
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Spins up a new thread to run a given effect for 'duration' seconds. NOTE: It will hold the thread 
                 even when the time is done so it's on the function to check for the run_effect and exit gracefully.
    INPUT: effect_func - Function ref that we will be using for our effect.
           duration - Number of seconds we will run this effect.
           args - Tuple of optional args that we can pass to our 'effect_func'
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def run_effect_for_x_seconds(self, effect_func, duration: int=10, args: tuple=()):
        self.run_effect = True

        thread = threading.Thread(target=effect_func, args=args)
        thread.start()
        time.sleep(duration)

        self.run_effect = False
        thread.join()
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: We often need the range of values we are working with given a certain axis. This function just finds
                 the min and max values for that given axis.
    INPUT: axis - X, Y, or Z (0, 1, 2), which axis we will be grabbing the min and max from.
    OUTPUT: Tuple of (min, max) value for the given 'axis'
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def find_min_max(self, axis: int) -> tuple[int, int]:
        min_val = sys.maxsize
        max_val = -sys.maxsize - 1
        for elem in coordinates:
            min_val = min(min_val, elem[axis])
            max_val = max(max_val, elem[axis])
        return min_val, max_val
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Turns 'off' all the LEDs ie just sets them all to (0, 0, 0).
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def turn_off(self) -> None:
        self.pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        self.led_controller.update_leds(self.pixel_data)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Runs a "rainbow" effect. The given 'axis' will define the "direction" of the color change.
    INPUT: axis - X, Y, or Z (0, 1, 2), which axis we will be changing the color against.
           step - Basically how 'fast' the effect moves. Needs trial and error.
           width - How "much" of the full color spectrum you see at one time. 
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""      
    def rainbow(self, axis:int, step:float, width:float) -> None:
        height = self.min_and_max[axis][1] - self.min_and_max[axis][0]
        
        hue_step = int(360 * step)
        dis_vals = [360*width*((coordinates[pixel][axis] + self.min_and_max[axis][0]) / height) 
                    for pixel in range(Settings.NUM_LEDS)]
        
        while self.run_effect:
            for hue in range(0, int(math.copysign(360, hue_step)), hue_step):
                for pixel in range(Settings.NUM_LEDS):
                    val = (hue + dis_vals[pixel]) % 360
                    self.pixel_data[pixel] = CH.gamma_correct(hue=val)
                self.led_controller.update_leds(self.pixel_data)
                
#################################################################################
#################################################################################
#################################################################################
   
    def plane(self, axis: int=0) -> None:
        fade_values = [0.0] * 650
        cur_hue = 0
        coords = coordinates
        
        while self.run_effect:
            cur_hue = random.randint(0, 360) / 360
            # Random rotation angles
            random_angles = [random.uniform(0, 360) for _ in range(3)]
            coords = [rotate_point(np.array(coord), random_angles) for coord in coords]

            min_val = sys.maxsize
            max_val = -sys.maxsize - 1
            for elem in coords:
                min_val = min(min_val, elem[0])
                max_val = max(max_val, elem[0])
            
            
            for height in range(int(min_val), int(max_val)+200, 10):
                for pixel in range(Settings.NUM_LEDS):
                    if coords[pixel][axis] > height and coords[pixel][axis] < height + 50:
                        fade_values[pixel] = 1.0
                        
                    if fade_values[pixel] > 0.001:
                        fade_values[pixel] = fade_values[pixel] / random.uniform(1.0, 1.3)
                        r, g, b = colorsys.hsv_to_rgb(cur_hue, 1.0, fade_values[pixel])
                        rgb = (r * 255, g * 255, b * 255)
                    else:
                        fade_values[pixel] = 0.0
                        rgb = (0, 0, 0)

                    self.pixel_data[pixel] = rgb
                        
                self.led_controller.update_leds(self.pixel_data)
       
        while any(value > 0.01 for value in fade_values):
            for pixel in range(Settings.NUM_LEDS):
                if fade_values[pixel] > 0.01:
                    fade_values[pixel] = fade_values[pixel] / random.uniform(1.0, 1.2)
                    r, g, b = colorsys.hsv_to_rgb(cur_hue, 1.0, fade_values[pixel])
                    self.pixel_data[pixel] = (r * 255, g * 255, b * 255)
                    
            self.led_controller.update_leds(self.pixel_data)
        
                
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Changes the entire LED strip to one single color and runs that color through the spectrum. No current
                 support for making it faster or slower. That is more so defined by the 'refresh_rate'
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def solid_color_rainbow(self) -> None:
        while self.run_effect:
            for hue in range(360):
                self.pixel_data = [CH.hue_to_rgb_corrected(hue)] * Settings.NUM_LEDS
                self.led_controller.update_leds(self.pixel_data)


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════