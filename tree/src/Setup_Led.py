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
from Coords import coordinates
from Led_Controller import LEDController
from helpers.Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Itterates over every LED and turns on each individually after each 'Enter' is pressed. Specifically used
             in our setup of the tree with the camera calibration code.
INPUT: NA
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def one_led():
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)
    
    for cur_led in range(Settings.NUM_LEDS):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        pixel_data[cur_led] = (255, 255, 255)
        led_controller.update_leds(pixel_data)
        input(f"LED: {cur_led} Press Enter to continue...")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Slides a "plane" across the given XYZ axis to help find outlier LEDs.
INPUT: axis - XYZ (0, 1, or 2) axis we will itterate over and show LEDs that intersect.
       width - How "wide" our plane is to better visualize out of place LEDs.
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def slide_grid(axis=0, width=50):
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)
    
    axis_coords = [coord[axis] for coord in coordinates]
    min_val, max_val = min(axis_coords), max(axis_coords)
    
    for val in range(min_val, max_val, width):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        for led in range(Settings.NUM_LEDS):
            if coordinates[led][axis] >= val and coordinates[led][axis] <= val + width:
                print(f"{led}: {val}")
                pixel_data[led] = (0, 0, 255)
        led_controller.update_leds(pixel_data)
        input(f"Showing {val}-{val+width}...")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Sometimes LED's go bad and have weird colors displayed. This just goes through our strip and let's you
             find the LED index with "relative" ease to add to our 'BAD_LEDS' list in Settings.
INPUT: starting_index - Which LED index we will start displaying from.
       ending_index - Which LED index to end at.
       step - How many LEDs we will display in batches.
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def find_bad_led(starting_index, ending_index, step):
    led_controller = LEDController()
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)
    
    for val in range(starting_index, ending_index, step):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        for led in range(val, val + step):
            pixel_data[led] = (0, 0, 255)
        led_controller.update_leds(pixel_data)
        input(f"Showing {val}-{val+step}...")


def main():
    one_led()
    # slide_grid(axis=1, width=50)
    # slide_grid(axis=2, width=50)
    # slide_grid(axis=3, width=50)
    # find_bad_led(0, Settings.NUM_LEDS, 10)

if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
