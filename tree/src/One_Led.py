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
import time

from Led_Controller import LEDController
from helpers.Settings import Settings


def main():
    led_controller = LEDController(refresh_rate_hz=35)
    pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
    led_controller.update_leds(pixel_data)
    
    for cur_led in range(Settings.NUM_LEDS):
        pixel_data = [(0, 0, 0)] * Settings.NUM_LEDS
        pixel_data[cur_led] = (255, 255, 255)
        led_controller.update_leds(pixel_data)
        input("Press Enter to continue...")
        

if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════