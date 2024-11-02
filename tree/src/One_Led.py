# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    ONE LED CALIBRATION                      CREATED: 2024-10-19          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# This is to be run with our calibration through the webcam to properly plot out where every single LED on the tree is.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys
import time

from Coords import coordinates
from Led_Controller import LEDController
from helpers.Settings import Settings


def find_min_max(axis: int) -> tuple[int, int]:
    min_val = sys.maxsize
    max_val = -sys.maxsize - 1
    for elem in coordinates:
        min_val = min(min_val, elem[axis])
        max_val = max(max_val, elem[axis])
    return min_val, max_val


def one_led():
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)
    
    # for cur_led in range(Settings.NUM_LEDS):
    for cur_led in range(390, 400):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        pixel_data[cur_led] = (255, 255, 255)
        led_controller.update_leds(pixel_data)
        input(f"LED: {cur_led} Press Enter to continue...")


def slide_grid(axis=0):
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)

    min_val, max_val = find_min_max(axis)
    print(min_val, max_val, max_val-min_val)

    for val in range(min_val, max_val, 50):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        for led in range(Settings.NUM_LEDS):
            if coordinates[led][axis] >= val and coordinates[led][axis] <= val + 50:
                print(f"{led}: {val}")
                pixel_data[led] = (0, 0, 255)
        led_controller.update_leds(pixel_data)
        input(f"Showing {val}-{val+50}...")

def find_bad_led():
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)

    for val in range(0, Settings.NUM_LEDS, 10):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        for led in range(val, val+10):
            pixel_data[led] = (0, 0, 255)
        led_controller.update_leds(pixel_data)
        input(f"Showing {val}-{val+10}...")
    
def adjust_coords():
    for coord in coordinates:
        coord[0] = coord[0]-664
        print(f", {coord}")


def main():
    one_led()
    # slide_grid(axis=1)
    # find_bad_led()
    # slide_grid(axis=2)
    # adjust_coords()

if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════