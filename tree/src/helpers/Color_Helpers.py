# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    COLOR HELPERS                            CREATED: 2027-10-18          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Various color helpers to do things like hue -> RGB conversions, gamma correction, and many others.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import colorsys
from helpers.Settings import Settings

def generate_hue_lookup_table():
    lookup_table = []
    for hue in range(360):
        r, g, b = colorsys.hsv_to_rgb((hue / 360.0), 1.0, 1.0)
        lookup_table.append((int((r ** Settings.GAMMA_RED) * 255)
                             , int((g ** Settings.GAMMA_GREEN) * 255)
                             , int((b ** Settings.GAMMA_BLUE) * 255)))
    return lookup_table

def generate_combined_rgb_lookup():
    return [(int((i / 255.0) ** Settings.GAMMA_RED * 255)
             , int((i / 255.0) ** Settings.GAMMA_GREEN * 255)
             , int((i / 255.0) ** Settings.GAMMA_BLUE * 255))
            for i in range(256)]

hue_lookup_table = generate_hue_lookup_table()
rgb_lookup_table = generate_combined_rgb_lookup()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def gamma_correct(hue=None, rgb=None):
    if hue is not None:
        return hue_lookup_table[int(hue % 360)]
    elif rgb is not None:
        return tuple(rgb_lookup_table[channel][idx] for idx, channel in enumerate(rgb))
    else:
        raise ValueError("Either 'hue' or 'rgb' must be provided.")


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════