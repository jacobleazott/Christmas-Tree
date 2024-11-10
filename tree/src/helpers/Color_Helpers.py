# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    COLOR HELPERS                            CREATED: 2024-10-18          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Various color helpers to do things like hue -> RGB conversions, gamma correction, and many others.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import numpy as np
from typing import Optional

from helpers.Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Generates a gamma corrected table for RGB values. The format is a 256 length list with a tuple of 3 ints.
             So you just look up each RGB value individually. ie. (100, 200, 1) gamma corrected would take the 100th
             element [0] for red, the 200th element [1] for blue, and the 1st element [2] for green. Giving you an RGB
             tuple that is gamma corrected according to our gamma correction values.
INPUT: NA
OUTPUT: RGB lookup table to gamma correct any int rgb tuple.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_combined_rgb_lookup() -> np.ndarray:
    table = np.zeros((256, 3), dtype=np.uint8)  # 256 rows, 3 columns (for R, G, B)
    
    for i in range(256):
        table[i] = [
            int((i / 255.0) ** Settings.GAMMA_RED * 255)      # Gamma corrected red
            , int((i / 255.0) ** Settings.GAMMA_GREEN * 255)  # Gamma corrected green
            , int((i / 255.0) ** Settings.GAMMA_BLUE * 255)   # Gamma corrected blue
        ]
    
    return table


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes a given hsv array of normalized values, converts them to RGB, and gamma corrects them.
INPUT: hsv_array - Np array of hsv values normalized between 0 and 1.
OUTPUT: Same size hsv_array, just with RGB values 0-255 gamma corrected.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def hsv_to_rgb_gamma_corrected(hsv_array: np.ndarray) -> np.ndarray:
    # Unpack the HSV array into separate H, S, V components
    h, s, v = hsv_array[:, 0], hsv_array[:, 1], hsv_array[:, 2]
    
    # Scale hue to [0, 6)
    h = h * 6
    i = np.floor(h).astype(int)  # integer part of h
    f = h - i  # fractional part of h
    
    # Calculate intermediate values for RGB
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    # Initialize RGB arrays
    rgb_array = np.zeros_like(hsv_array)
    
    # Assign RGB values based on the sector
    i_mod = i % 6
    rgb_array[i_mod == 0] = np.stack([v, t, p], axis=-1)[i_mod == 0]
    rgb_array[i_mod == 1] = np.stack([q, v, p], axis=-1)[i_mod == 1]
    rgb_array[i_mod == 2] = np.stack([p, v, t], axis=-1)[i_mod == 2]
    rgb_array[i_mod == 3] = np.stack([p, q, v], axis=-1)[i_mod == 3]
    rgb_array[i_mod == 4] = np.stack([t, p, v], axis=-1)[i_mod == 4]
    rgb_array[i_mod == 5] = np.stack([v, p, q], axis=-1)[i_mod == 5]
    
    # Scale to 8-bit RGB (0-255)
    rgb_array = (rgb_array * 255).astype(np.uint8)
    
    # Apply gamma correction using the lookup table
    # Correct the RGB channels by using advanced indexing
    r_corrected = rgb_lookup_table[rgb_array[:, 0], 0]
    g_corrected = rgb_lookup_table[rgb_array[:, 1], 1]
    b_corrected = rgb_lookup_table[rgb_array[:, 2], 2]
    
    # Stack corrected channels back together
    rgb_corrected = np.stack([r_corrected, g_corrected, b_corrected], axis=-1)
    
    return rgb_corrected


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Wrapper to blend_hsv_vectorized to allow for 'hsv1' and 'hsv2' to be single values, arrays, or a mix of
             both to properly apply blending across an entire array of hsv values.
INPUT: hsv1 - Single hsv value or an array of values to blend with 'hsv2'
       hsv2 - Single hsv value to blend with 'hsv1'. If an array it needs to be same size as array of 'hsv1'.
       sat_val - Optional saturation override.
       val_val - Optional value override.
OUTPUT: Np array of blended normalized HSV value.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def blend_hsv(hsv1: np.ndarray, hsv2: np.ndarray,
              sat_val: Optional[float]=None, val_val: Optional[float]=None) -> np.ndarray:
    # Convert hsv1 to a NumPy array if it's not already
    hsv1 = np.array(hsv1) if not isinstance(hsv1, np.ndarray) else hsv1
    
    # Handle the case where hsv2 is a single value
    if hsv2.ndim == 1:
        # If hsv2 is a single value (1, 3), expand it to match the shape of hsv1
        hsv2 = np.repeat(hsv2[np.newaxis, :], hsv1.shape[0], axis=0)
    
    # Now both hsv1 and hsv2 should have compatible shapes (n, 3)
    blended_hsv = blend_hsv_vectorized(hsv1, hsv2, sat_val=sat_val, val_val=val_val)
    
    return blended_hsv


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes two given Normalized HSV values and "blends" them. It offers the ability to disregard saturation
             and value if you want to override that value yourself. Important note that it weights the average of the
             resulting hue based upon the ratio of the two hsv's values. ie. a bright red and a dim blue is more red
             leaning then a true split between.
INPUT: hsv1 - Array of hsv values to blend with 'hsv2'
       hsv2 - Array of hsv value to blend with 'hsv1'.
       sat_val - Optional saturation override.
       val_val - Optional value override.
OUTPUT: Np array of blended normalized HSV value.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def blend_hsv_vectorized(hsv1: np.ndarray, hsv2: np.ndarray,
                         sat_val: Optional[float]=None,
                         val_val: Optional[float]=None) -> np.ndarray:
    h1, s1, v1 = hsv1[:, 0], hsv1[:, 1], hsv1[:, 2]
    h2, s2, v2 = hsv2[:, 0], hsv2[:, 1], hsv2[:, 2]
    
    # Compute weights based on brightness
    total_value = v1 + v2
    weight1 = v1 / total_value
    weight2 = v2 / total_value
    
    # Convert hues to radians and calculate weighted circular mean
    h1_rad = h1 * 2 * np.pi
    h2_rad = h2 * 2 * np.pi
    avg_hue_rad = np.arctan2(weight1 * np.sin(h1_rad) + weight2 * np.sin(h2_rad),
                             weight1 * np.cos(h1_rad) + weight2 * np.cos(h2_rad))
    
    avg_hue = (avg_hue_rad / (2 * np.pi)) % 1.0  # Normalize to 0-1 range
    
    # Calculate weighted averages for saturation and value
    avg_saturation = sat_val if sat_val is not None else s1 * weight1 + s2 * weight2
    avg_value = val_val if val_val is not None else v1 * weight1 + v2 * weight2
    
    return np.column_stack((avg_hue, avg_saturation, avg_value))


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
        rand_hue = np.random.uniform(0, lower_bound) if np.random.rand() < 0.5 else np.random.uniform(upper_bound, 1)
    else:
        # Wraps around the 1.0 boundary, so generate a random hue in the range [upper_bound, lower_bound)
        rand_hue = np.random.uniform(upper_bound, lower_bound)
    
    return rand_hue


# Generate Lookup Tables On Startup
rgb_lookup_table = generate_combined_rgb_lookup()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
