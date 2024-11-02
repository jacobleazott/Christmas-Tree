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
import math
import random
from helpers.Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Generates a hue gamma lookup table to use for gamma correction of hue values. It defaults to full
             saturation and value.
INPUT: NA
OUTPUT: Lookup table for any given integer hue value to it's gamma corrected rgb value.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_hue_lookup_table():
    lookup_table = []
    for hue in range(360):
        r, g, b = colorsys.hsv_to_rgb((hue / 360.0), 1.0, 1.0)
        lookup_table.append((int((r ** Settings.GAMMA_RED) * 255)
                             , int((g ** Settings.GAMMA_GREEN) * 255)
                             , int((b ** Settings.GAMMA_BLUE) * 255)))
    return lookup_table


def get_gamma_corrected_rgb(hsv):
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return (
        int((r ** Settings.GAMMA_RED) * 255),
        int((g ** Settings.GAMMA_GREEN) * 255),
        int((b ** Settings.GAMMA_BLUE) * 255)
    )


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_combined_rgb_lookup():
    return [(int((i / 255.0) ** Settings.GAMMA_RED * 255)
             , int((i / 255.0) ** Settings.GAMMA_GREEN * 255)
             , int((i / 255.0) ** Settings.GAMMA_BLUE * 255))
            for i in range(256)]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def gamma_correct(hsv=None, rgb=None):
    if hsv is not None:
        # return hue_lookup_table[int(hue % 360)]
        return get_gamma_corrected_rgb(hsv)
    elif rgb is not None:
        return tuple(rgb_lookup_table[channel][idx] for idx, channel in enumerate(rgb))
    else:
        raise ValueError("Either 'hsv' or 'rgb' must be provided.")
    
    
def blend_hsv(hsv1, hsv2, ignore_sat=False, ignore_val=False):
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    # Compute weights based on brightness
    total_value = v1 + v2
    weight1 = v1 / total_value
    weight2 = v2 / total_value

    # Convert hues to degrees for circular blending
    h1_deg = h1 * 360
    h2_deg = h2 * 360

    # Calculate weighted average hue using circular mean
    avg_hue_deg = math.degrees(math.atan2(
        weight1 * math.sin(math.radians(h1_deg)) + weight2 * math.sin(math.radians(h2_deg)),
        weight1 * math.cos(math.radians(h1_deg)) + weight2 * math.cos(math.radians(h2_deg))
    ))
    avg_hue_deg = (avg_hue_deg + 360) % 360  # Normalize to 0-360 range
    avg_hue = avg_hue_deg / 360  # Convert back to 0-1 range
    
    # Calculate weighted averages for saturation and value
    avg_saturation = 1.0
    avg_value = 1.0
    
    if not ignore_sat:
        avg_saturation = s1 * weight1 + s2 * weight2
        
    if not ignore_val:
        avg_value = v1 * weight1 + v2 * weight2

    return [avg_hue, avg_saturation, avg_value]

def random_hue_away_from(hue, min_distance=0.1):
    # Calculate the boundaries of the forbidden range
    lower_bound = (hue - min_distance) % 1.0
    upper_bound = (hue + min_distance) % 1.0

    if lower_bound < upper_bound:
        # Generate a random hue in the range [0, lower_bound) or [upper_bound, 1)
        rand_hue = random.uniform(0, lower_bound) if random.random() < 0.5 else random.uniform(upper_bound, 1)
    else:
        # Wraps around the 1.0 boundary, so generate a random hue in the range [upper_bound, lower_bound)
        rand_hue = random.uniform(upper_bound, lower_bound)

    return rand_hue


# Generate Lookup Tables On Startup
hue_lookup_table = generate_hue_lookup_table()
rgb_lookup_table = generate_combined_rgb_lookup()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════