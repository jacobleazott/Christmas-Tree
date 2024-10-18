# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    LED CONTROLLER                           CREATED: 2024-10-17          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Basic utility helper to handle the updates to led strips using the neopixel library.
# 
# I think the main idea is to handle our threading for updating the pixels, and handling any color format that we
#   could think to pass in. On top of that enabling things like gamma correction or other fun things like that.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import time
import board
import neopixel
import sys

from coords import gamma_table, coordinates

from Settings import Settings

# Other Interesting Methods/ Ideas For This File
#   Color 'Filler' just like turning every led in the strip black, turn the entire strip (or maybe a section) to a given color


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LedController():
    
    def __init__(self) -> None:
        self.pixels = neopixel.NeoPixel(Settings.LED_PIN
                                        , Settings.NUM_LEDS
                                        , brightness=Settings.LED_BRIGHTNESS
                                        , auto_write=False
                                        , pixel_order=Settings.LED_ORDER)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def update_pixels(self, pixel_array: list) -> None:
        # Probably wanna do this by threading if we wanted to be smart, but that means we should implement some checks
        #   so that if we call update_pixels again before everything is updated we log some error 
        
        # Also we will probably want to accept a few different types of values, maybe accept hsv, hue, rgb, hex.
        # We also want a way to adjust gamma so not sure if we want that passed in as a setting, by default, in __init__
        #   but that will just add some conditional logic here.
        for idx, pixel_val in enumerate(pixel_array):
            self.pixels[idx] = pixel_val
        self.pixels.show()
        
    def turn_off(self) -> None:
        # Probaby wanna update this to just pass in an array of 0's to update_pixels
        for led in range(Settings.NUM_LEDS):
            self.pixels[led] = [0, 0, 0]
        self.pixels.show()
        
    
    
    # def gamma(uncor_color):
    #     return gamma_table[int(uncor_color[0])], gamma_table[int(uncor_color[1])], gamma_table[int(uncor_color[2])]

    # def hue_to_rgb(hue_value):
    #     x = int(255 * (1 - abs(((hue_value / 60) % 2) - 1)))
    #     if hue_value < 60:
    #         value = (255, x, 0)
    #     elif hue_value < 120:
    #         value = (x, 255, 0)
    #     elif hue_value < 180:
    #         value = (0, 255, x)
    #     elif hue_value < 240:
    #         value = (0, x, 255)
    #     elif hue_value < 300:
    #         value = (x, 0, 255)
    #     else:
    #         value = (255, 0, x)
    #     return value

    # def hue_to_rgb_corrected(hue_value):
    #     return gamma(hue_to_rgb(hue_value))


def main():
    print("Not Implemented")


if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════