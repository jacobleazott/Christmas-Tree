import time
import board
import neopixel
import sys

from coords import gamma_table, coordinates

num_pixels = 650
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

for i in range(0, num_pixels):
    pixels[i] = [0, 0, 0]
pixels.show()