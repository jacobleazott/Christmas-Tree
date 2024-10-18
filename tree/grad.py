import time
import board
import neopixel
import sys

from coords import gamma_table, coordinates

num_pixels = 601
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)


def gamma(uncor_color):
    return gamma_table[int(uncor_color[0])], gamma_table[int(uncor_color[1])], gamma_table[int(uncor_color[2])]

def hue_to_rgb(hue_value):
    x = int(255 * (1 - abs(((hue_value / 60) % 2) - 1)))
    if hue_value < 60:
        value = (255, x, 0)
    elif hue_value < 120:
        value = (x, 255, 0)
    elif hue_value < 180:
        value = (0, 255, x)
    elif hue_value < 240:
        value = (0, x, 255)
    elif hue_value < 300:
        value = (x, 0, 255)
    else:
        value = (255, 0, x)
    return value

def hue_to_rgb_corrected(hue_value):
    return gamma(hue_to_rgb(hue_value))

def find_min_max(element):
    min_val = sys.maxsize
    max_val = -sys.maxsize - 1
    for elem in coordinates:
        min_val = min(min_val, elem[element])
        max_val = max(max_val, elem[element])
    return min_val, max_val

# axis - 0, 1, or 2 ie. x, y, z
# step - how "fast" it goes, it is in relation to height so regardless of pixel dimensions it "should" work, might
#        be worth to find an adaptive way to calculate time per calculation and then know how many calculations it would
#        take to complete 1 cycle, then have the user provide a "time to complete 1 cycle" and work that out
# width - how "much" of the hue specturm you see, 1 being 1 full 0-360 range, 0.5 would mean only half (180) is visible at any given time
def run_rainbow(axis, step, width):
    global min_and_max
    height = ( min_and_max[axis][1] - min_and_max[axis][0] )
    height_hue_step = 2 * width * ( 360 / height )
    for i in range( 0, int(height / (2 * width)), int(height * step) ):
        for pixel in range( num_pixels ):
            val = (abs(coordinates[pixel][axis] - i ) * height_hue_step) % 360
            pixels[pixel] = hue_to_rgb_corrected( val )
        pixels.show()

min_and_max = (find_min_max(0), find_min_max(1), find_min_max(2))

while True:
    run_rainbow(0, 0.01, 0.75)
