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
import colorsys

import helpers.Color_Helpers as CH
import helpers.Math_Helpers as MH

from helpers.decorators import *
from helpers.Settings import Settings
from Coords import coordinates
from Led_Controller import LEDController        


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Collection of LED effects and the handler of our LEDController.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDEffects(LogAllMethods):
    
    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        
        self.pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        self.min_and_max = (self.find_min_max(coordinates, 0), self.find_min_max(coordinates, 1), self.find_min_max(coordinates, 2))
        
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

        thread = threading.Thread(target=effect_func, args=args, daemon=True)
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
    def find_min_max(self, coords, axis: int) -> tuple[int, int]:
        axis_coords = [coord[axis] for coord in coords]
        return min(axis_coords), max(axis_coords)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Turns 'off' all the LEDs ie just sets them all to (0, 0, 0).
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def turn_off(self) -> None:
        self.pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        self.led_controller.update_leds(self.pixel_data)
    
    
    def _rainbow(self, hue_step, distance_values):
        for hue in range(0, int(math.copysign(360, hue_step)), hue_step):
            for pixel in range(Settings.NUM_LEDS):
                val = (hue + distance_values[pixel]) % 360
                self.pixel_data[pixel] = CH.gamma_correct(hsv=(val / 360.0, 1.0, 1.0))
            self.led_controller.update_leds(self.pixel_data)
                
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Runs a "rainbow" effect. The given 'axis' will define the "direction" of the color change.
    INPUT: axis - X, Y, or Z (0, 1, 2), which axis we will be changing the color against.
           step - Basically how 'fast' the effect moves. Needs trial and error.
           width - How "much" of the full color spectrum you see at one time. 
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""      
    def axis_rainbow(self, axis:int, step:float, width:float) -> None:
        height = self.min_and_max[axis][1] - self.min_and_max[axis][0]
        hue_step = int(360 * step)
        dis_vals = [360*width*((coordinates[pixel][axis] + self.min_and_max[axis][0]) / height) 
                    for pixel in range(Settings.NUM_LEDS)]
        
        while self.run_effect:
            self._rainbow(hue_step, dis_vals)

    def radial_rainbow(self, axis:int, step:int, width:float) -> None:
        coords = MH.to_polar_coords(coordinates, axis)
        dis_vals = [width*(coords[pixel][1]) for pixel in range(Settings.NUM_LEDS)]
        
        while self.run_effect:
           self._rainbow(step, dis_vals)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def random_plane(self, step) -> None:
        fade_values = [[0.0, 0.0, 0.0]] * Settings.NUM_LEDS
        cur_hue = random.uniform(0.0, 1.0)
        coords = coordinates
        
        """Helper function to update pixel colors based on fade values."""
        def _fade_helper():
            for pixel, fade in enumerate(fade_values):
                if fade[2] > 0.001:
                    fade[2] /= random.uniform(1.0, 1.3)  # Apply fade
                    self.pixel_data[pixel] = CH.gamma_correct(hsv=fade)
                else: # Reset if too dim
                    fade_values[pixel] = [0.0, 0.0, 0.0]  
                    self.pixel_data[pixel] = (0, 0, 0)

            self.led_controller.update_leds(self.pixel_data)
        
        while self.run_effect:
            # Rotate coordinates randomly around three axes
            random_angles = [random.uniform(0, 360) for _ in range(3)]
            coords = [MH.rotate_point(coord, random_angles) for coord in coords]

            # Grab min and max along the given axis
            min_val, max_val = self.find_min_max(coords, 0)

            for height in range(int(min_val), int(max_val), step):
                for pixel in range(Settings.NUM_LEDS):
                    # Apply hue or fade effect based on pixel height range
                    if height <= coords[pixel][0] < height + 50:
                        fade_values[pixel] = CH.blend_hsv(
                            fade_values[pixel], [cur_hue, 1.0, 1.0],
                            ignore_sat=True, ignore_val=True
                        ) if fade_values[pixel][2] >= 0.01 else [cur_hue, 1.0, 1.0]
                        
                # Update the pixels and fade values
                _fade_helper()
            
            # Randomize the hue for the next iteration
            cur_hue = CH.random_hue_away_from(cur_hue)

        # Gracefully fade out remaining pixels
        while any(fade[2] > 0.01 for fade in fade_values):
            _fade_helper()
    
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


if __name__ == "__main__":
    led_effects = LEDEffects()
    led_effects.turn_off()
    time.sleep(0.2)


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════