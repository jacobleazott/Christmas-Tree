# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    SETTINGS AND CONSTANTS                   CREATED: 2024-10-17          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# This file solely holds our SettingsClass which is just a collection of "configurable" values that a user of the
#   project may want to change. It offers a single location for all files to reference. It utilizes a frozen dataclass
#   which means when we instantiate it as 'Settings' no inheriter can ever change these values. In this way we make a
#   common location for immutable settings during runtime. I still leave the discretion to include constants in
#   individual files for 'magic' numbers that should NEVER change and shouldn't be 'easily' changed through these
#   configurations.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
from dataclasses import dataclass

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Class that holds all of our user configurable settings/ constants for the project.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@dataclass(frozen=True)
class SettingsClass:
    # LED Strip Settings
    NUM_LEDS: int       = 650       # Number of LED pixels
    LED_FPS: int        = 35        # Number of updates per second for our LED strip.
    LED_PIN: int        = 18        # GPIO pin connected to the pixels (must support PWM or PCM)
    LED_BRIGHTNESS: int = 40        # Brightness of LEDs (0-255)
    LED_FREQ_HZ: int    = 800000    # LED signal frequency in hertz (usually 800kHz)
    LED_DMA: int        = 10        # DMA channel to use for generating signal (try 10)
    LED_INVERT: bool    = False     # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL: int    = 0         # Channel (default is 0)
    LED_ORDER: str      = "GRB"     # Pixel color order (typically 'GRB')
    
    # Internal Implementation Settings
    UPDATE_QUEUE_SIZE: int = 120    # Number of updates we can "preprocess" before waiting to calculate further
    
    GAMMA_RED: float    = 2.0       # Gamma correction value for 'red'.
    GAMMA_GREEN: float  = 1.8       # Gamma correction value for 'green'.
    GAMMA_BLUE: float   = 1.9       # Gamma correction value for 'blue'.
    
    BAD_LEDS: tuple[int] = (395,)    # Tuple of LED's we should never turn on.
    
    # Logging Settings
    FUNCTION_ARG_LOGGING_LEVEL: int = 15

Settings = SettingsClass()

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
