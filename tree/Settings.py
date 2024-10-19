# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    SETTINGS AND CONSTANTS                   CREATED: 2024-10-17          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# 
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import board
import neopixel
from dataclasses import dataclass


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Class that holds all of our user configurable settings/ constants for the project.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@dataclass(frozen=True)
class SettingsClass:
    LED_PIN: int = 18                 # GPIO pin connected to the pixels (must support PWM or PCM)
    NUM_LEDS: int = 100               # Number of LED pixels
    LED_BRIGHTNESS: int = 128         # Brightness of LEDs (0-255)
    LED_FREQ_HZ: int = 800000         # LED signal frequency in hertz (usually 800kHz)
    LED_DMA: int = 10                 # DMA channel to use for generating signal (try 10)
    LED_INVERT: bool = False          # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL: int = 0              # Channel (default is 0)
    LED_ORDER: str = 'GRB'            # Pixel color order (typically 'GRB' for
    
    # This has cost me so much sanity. Don't make this greater than 10 on a rpi 3b+
    UPDATE_QUEUE_SIZE: int = 20       # Number of updates we can "preprocess" before waiting to calculate further

    # Logging Settings
    FUNCTION_ARG_LOGGING_LEVEL: int = 15

Settings = SettingsClass()

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════