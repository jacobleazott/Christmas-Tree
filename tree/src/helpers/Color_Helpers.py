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
from numbers import Real

from helpers.Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Generates a gamma corrected table for RGB values. The format is a 256 length list with a tuple of 3 ints.
             So you just look up each RGB value individually. ie. (100, 200, 1) gamma corrected would take the 100th
             element [0] for red, the 200th element [1] for blue, and the 1st element [2] for green. Giving you an RGB
             tuple that is gamma corrected according to our gamma correction values.
INPUT: NA
OUTPUT: RGB lookup table to gamma correct any int rgb tuple.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_combined_rgb_lookup() -> list[tuple[Real, Real, Real]]:
    return [(int((i / 255.0) ** Settings.GAMMA_RED * 255)
             , int((i / 255.0) ** Settings.GAMMA_GREEN * 255)
             , int((i / 255.0) ** Settings.GAMMA_BLUE * 255))
            for i in range(256)]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes a given 'hsv' or 'rgb' value and returns the gamma corrected RGB value.
INPUT: hsv - Tuple of Normalized (0.0->1.0) HSV values.
       rgb - Tuple of int (0->255) RGB values.
OUTPUT: Tuple of gamma corrected RGB (0->255) values.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def gamma_correct(hsv: tuple[float, float, float]=None, rgb: tuple[int, int, int]=None) -> tuple[Real, Real, Real]:
    if hsv is None and rgb is None:
        raise ValueError("Either 'hsv' or 'rgb' must be provided.")
    
    res_rgb = rgb
    if hsv is not None:
        r, g, b = colorsys.hsv_to_rgb(*hsv)
        res_rgb = (int(r * 255), int(g * 255), int(b * 255))

    return tuple(rgb_lookup_table[int(channel)][idx] for idx, channel in enumerate(res_rgb))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes two given Normalized HSV values and "blends" them. It offers the ability to disregard saturation
             and value if you want to override that value yourself. Important note that it weights the average of the
             resulting hue based upon the ratio of the two hsv's values. ie. a bright red and a dim blue is more red
             leaning then a true split between.
INPUT: hsv1 and hsv2 - Normalized HSV values we will be blending.
       sat_val - Saturation value we can supply if we wish to disregard averaging the 'hsv1' and 'hsv2' values.
       val_val - Value value we can supply if we wish to disregard averaging the 'hsv1' and 'hsv2' values.
OUTPUT: Tuple of blended normalized HSV value.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def blend_hsv(hsv1: tuple[float, float, float], hsv2: tuple[float, float, float]
              , sat_val: float=None, val_val: float=None) -> tuple[float, float, float]:
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2
    
    # Compute weights based on brightness
    total_value = v1 + v2
    if total_value == 0:
        return hsv1  # Avoid division by zero; return first color if both are black.

    weight1 = v1 / total_value
    weight2 = v2 / total_value

    # Convert hues to radians and calculate weighted circular mean
    h1_rad = h1 * 2 * math.pi
    h2_rad = h2 * 2 * math.pi
    avg_hue_rad = math.atan2(weight1 * math.sin(h1_rad) + weight2 * math.sin(h2_rad)
                           , weight1 * math.cos(h1_rad) + weight2 * math.cos(h2_rad))
    
    avg_hue = avg_hue_rad / (2 * math.pi) % 1.0  # Normalize to 0-1 range

    # Calculate weighted averages for saturation and value, using optional overrides
    avg_saturation = sat_val if sat_val is not None else s1 * weight1 + s2 * weight2
    avg_value = val_val if val_val is not None else v1 * weight1 + v2 * weight2

    return avg_hue, avg_saturation, avg_value


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Given a 'hue' we will generate a random hue that is at least 'min_distance' away so you don't end up with
             colors being the same back to back in animations.
INPUT: hue - Normalized hue value of what we want to be randomly "away" from.
       min_distance - How 'far' minimally away we will be from our givne 'hue'.
OUTPUT: Random hue value at least 'min_distance' away from 'hue'.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def random_hue_away_from(hue: float, min_distance: float=0.1) -> float:
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
rgb_lookup_table = generate_combined_rgb_lookup()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════