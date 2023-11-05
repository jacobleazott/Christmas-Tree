import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 650

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

curr_led = 1
pixels[0] = [255, 255, 255]
pixels.show()

while True:
    input("Press Enter to continue...")
    pixels[curr_led - 1] = [0, 0, 0]
    pixels[curr_led] = [255, 255, 255]
    curr_led += 1
    pixels.show()
