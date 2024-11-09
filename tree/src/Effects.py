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
from numbers import Real

import numpy as np

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
    
    def __init__(self, logger: logging.Logger=None) -> None:
        self.logger = logger if logger is not None else logging.getLogger()
        
        self.pixel_data = np.zeros((Settings.NUM_LEDS, 3), dtype=np.uint8)
        
        self.min_and_max = (
            (np.min(coordinates[:, 0]), np.max(coordinates[:, 0])),  # Min/Max for x-axis
            (np.min(coordinates[:, 1]), np.max(coordinates[:, 1])),  # Min/Max for y-axis
            (np.min(coordinates[:, 2]), np.max(coordinates[:, 2])))  # Min/Max for z-axis
        
        self.led_controller = LEDController(logger=self.logger)
        
        self.run_effect = True
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Spins up a new thread to run a given effect for 'duration' seconds. NOTE: It will hold the thread 
                 even when the time is done so it's on the function to check for the run_effect and exit gracefully.
    INPUT: effect_func - Function ref that we will be using for our effect.
           duration - Number of seconds we will run this effect.
           args - Tuple of optional args that we can pass to our 'effect_func'
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def run_effect_for_x_seconds(self, effect_func, duration: int=10, args: tuple=()) -> None:
        self.run_effect = True

        thread = threading.Thread(target=effect_func, args=args, daemon=True)
        thread.start()
        time.sleep(duration)

        self.run_effect = False
        thread.join()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Turns 'off' all the LEDs ie just sets them all to (0, 0, 0).
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def turn_off(self) -> None:
        self.pixel_data = np.zeros((Settings.NUM_LEDS, 3), dtype=np.uint8)
        self.led_controller.update_leds(self.pixel_data)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Generic rainbow generator that takes a given 'hue_step' and uses the 'distance_values' to know how
                 'far' the current hue is from our base hue. We then can calculate what hue each pixel should be since
                 we know the 'step' it takes for each given unit and how many units it is away from 'distance_values'.
    INPUT: hue_step - How much each given 'unit' of distance correlates to a change in hue. For example we wanted to 
                      itterate over 100 evenly spaced LEDs and have 1 full spectrum. The 'hue_step' would be 100/360.
           distance_values - The 'unit' distance each pixel is away from our reference point we animate from.
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def _rainbow(self, hue_step: int, distance_values: list[Real]) -> None:
        step_size = hue_step / 360.0
    
        # Generate all normalized hue values
        num_steps = int(abs(1.0 / step_size))
        normalized_hues = np.linspace(0.0, np.copysign(1.0, step_size), num_steps, endpoint=False)
        
        # Calculate every distance value pair for our number of steps and number of LEDs
        hues_matrix = (normalized_hues[:, None] + distance_values) % 1.0  # Shape: (num_steps, NUM_LEDS)

        # Stack hues and SV values to create the full HSV array for all frames
        sv_values = np.ones_like(hues_matrix)
        hsv_values = np.stack((hues_matrix, sv_values, sv_values), axis=-1)  # Shape: (num_steps, NUM_LEDS, 3)
        
        # Convert all HSV frames to gamma corrected RGB values
        rgb_frames = CH.hsv_to_rgb_gamma_corrected(hsv_values.reshape(-1, 3)).reshape(num_steps, -1, 3)

        self.led_controller.update_leds(rgb_frames)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Runs a "rainbow" effect on the cartesian coords. The given 'axis' will define the "direction" change.
    INPUT: axis - X, Y, or Z (0, 1, 2), which axis we will be changing the color against.
           step - Basically how 'fast' the effect moves. Needs trial and error.
           width - How "much" of the full color spectrum you see at one time. 
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""      
    def axis_rainbow(self, axis:int, step:Real, width:Real) -> None:
        height = self.min_and_max[axis][1] - self.min_and_max[axis][0]
        dis_vals = width * ((coordinates[:, axis] + self.min_and_max[axis][0]) / height)
        
        while self.run_effect:
            self._rainbow(360 * step, dis_vals)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Runs a "rainbow" effect on 2D polar coords. The specified 'axis' being the one we "ignore". It then
                 simply runs on the theta portion of our polar coord with no regard to radius.
    INPUT: axis - X, Y, or Z (0, 1, 2), which axis we will be disregarding to compute our polar coords.
           step - Basically how 'fast' the effect moves. Needs trial and error.
           width - How "much" of the full color spectrum you see at one time. 
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def radial_rainbow(self, axis:int, step:int, width:Real) -> None:
        dis_vals = (width * (MH.convert_3D_coords_to_2D_polar(coordinates, axis)[:, 1] / 360.0)) % 1.0

        while self.run_effect:
           self._rainbow(step, dis_vals)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Sweeps a plane across the tree of a random color and random orientation. Also fades the plane as it 
                 passes through.
    INPUT: steps - How "fast" the plane travels across the tree. Needs trial and error.
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def random_plane(self, steps: int) -> None:
        # Values are normalized between 0.0 and 1.0
        hsv_values = np.zeros((Settings.NUM_LEDS, 3), dtype=np.float32)
        target_hsv = np.array([random.uniform(0.0, 1.0), 1.0, 1.0])
        fade_threshold = 0.1

        """Helper function to fade, gamma correct, and limit brightness of our LEDs."""
        def _fade_helper():
            fade_mask = hsv_values[:, 2] > fade_threshold # Only need to fade values above threshold.
            hsv_values[~fade_mask] = [0.0, 0.0, 0.0] # Reset anything that's below our threshold

            # Define a unique fade value for each pixel.
            fade_factors = np.random.uniform(1.0, 1.2, size=hsv_values.shape[0])

            # Apply fade only to pixels within our mask.
            hsv_values[fade_mask, 2] /= fade_factors[fade_mask]
            
            self.pixel_data = CH.hsv_to_rgb_gamma_corrected(hsv_values)
            self.led_controller.update_leds(self.pixel_data)
        
        while self.run_effect:
            # Rotate all coordinates at once
            coords = MH.rotate_coordinates(coordinates, np.random.uniform(0, 2 * np.pi, 3))
            height_range = np.linspace(coords[:, 0].min(), coords[:, 0].max(), steps)
            
            for height in height_range:
                in_plane_mask = (coords[:, 0] >= height) & (coords[:, 0] < height + 50)
                value_mask = hsv_values[:, 2] > fade_threshold
                # We only want to blend values that meet brightness threshold and intersect our plane
                combined_mask = in_plane_mask & value_mask

                # For these pixels, apply blending or set to the new hue
                hsv_values[combined_mask] = CH.blend_hsv(hsv_values[combined_mask], target_hsv)

                # For the rest of the pixels that are within our plane but didn't need blending, set directly to new hue
                hsv_values[in_plane_mask & ~value_mask] = target_hsv

                _fade_helper()

            # Randomize the hue for the next iteration
            target_hsv = np.array([CH.random_hue_away_from(target_hsv[0]), 1.0, 1.0])
            
        # Gracefully fade out remaining pixels
        while any(fade[2] > fade_threshold for fade in hsv_values):
            _fade_helper()
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Changes the entire LED strip to one single color and runs that color through the spectrum.
    INPUT: step - How "fast" the animation changes.
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def solid_color_rainbow(self, step: int) -> None:
        while self.run_effect:
            hues = np.arange(0, 360, step) / 360.0  
            hsv_values = np.zeros((len(hues), 3), dtype=np.float16)
            hsv_values[:, 0] = hues  # Hue
            hsv_values[:, 1] = 1.0   # Saturation (constant)
            hsv_values[:, 2] = 1.0   # Value (constant)
            
            rgb_frames = CH.hsv_to_rgb_gamma_corrected(hsv_values)
            rgb_leds = np.transpose(np.tile(rgb_frames, (Settings.NUM_LEDS, 1, 1)), (1, 0, 2)) 
            
            # Update the LEDs with the newly calculated pixel data
            self.led_controller.update_leds(rgb_leds)


if __name__ == "__main__":
    led_effects = LEDEffects()
    led_effects.turn_off()
    time.sleep(0.2)


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════