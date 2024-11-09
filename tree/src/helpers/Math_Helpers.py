# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    MATH HELPERS                             CREATED: 2024-11-01          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Various math helpers we use a lot, like rotating points or converting between polar and cartesian.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import math
import numpy as np
from numbers import Real

import time

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Given a single XYZ 'point', rotate it around the origin with XYZ parts of 'angles' 
INPUT: point - XYZ coord of the point we will be rotating.
       angles - XYZ rotation degrees we will apply to our 'point'.
OUTPUT: Rotated XYZ coordiante.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def rotate_point(point: tuple[Real, Real, Real], angles: tuple[Real, Real, Real]) -> tuple[Real, Real, Real]:
    point = np.array(point)
    
    # Convert angles from degrees to radians
    rx, ry, rz = np.radians(angles)
    
    # Precompute sin and cos values
    cos_rx, sin_rx = np.cos(rx), np.sin(rx)
    cos_ry, sin_ry = np.cos(ry), np.sin(ry)
    cos_rz, sin_rz = np.cos(rz), np.sin(rz)

    # Directly compute the combined rotation matrix R
    R = np.array([
        [cos_ry * cos_rz, -cos_ry * sin_rz, sin_ry],
        [sin_rx * sin_ry * cos_rz + cos_rx * sin_rz, -sin_rx * sin_ry * sin_rz + cos_rx * cos_rz, -sin_rx * cos_ry],
        [-cos_rx * sin_ry * cos_rz + sin_rx * sin_rz, cos_rx * sin_ry * sin_rz + sin_rx * cos_rz, cos_rx * cos_ry]
    ])
    
    rotated_point = R @ point
    return np.rint(rotated_point)


import numpy as np

def rotate_coordinates(coords: np.ndarray, angles: np.ndarray) -> np.ndarray:
    """
    Rotates a set of 3D Cartesian coordinates by three angles on the X, Y, and Z axes respectively.

    Args:
    - coords (np.ndarray): An array of shape (n, 3), where n is the number of coordinates.
    - angles (np.ndarray): An array of shape (3,), containing the rotation angles in radians for [theta_x, theta_y, theta_z].

    Returns:
    - np.ndarray: The rotated coordinates of shape (n, 3).
    """
    # Extract angles
    theta_x, theta_y, theta_z = angles

    # Rotation matrices
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x)],
        [0, np.sin(theta_x), np.cos(theta_x)]
    ])

    Ry = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])

    Rz = np.array([
        [np.cos(theta_z), -np.sin(theta_z), 0],
        [np.sin(theta_z), np.cos(theta_z), 0],
        [0, 0, 1]
    ])

    # Combined rotation matrix
    R = Rz @ Ry @ Rx  # Matrix multiplication in the correct order

    # Apply rotation to each coordinate (coords is shape (n, 3), R is 3x3)
    rotated_coords = np.dot(coords, R.T)  # Dot product for each coordinate

    return rotated_coords



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes a givne list of cartesian 'coords' and converts them into polar coords ignoring the given 'axis'.
INPUT: coords - XYZ values of our cartestion coordinates we will be converting.
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def to_2D_polar_coords(coords: np.ndarray) -> np.ndarray:
    x, y = coords[:, 0], coords[:, 1]
    
    r = np.hypot(x, y)  # Equivalent to sqrt(x**2 + y**2), more efficient
    theta_degrees = np.degrees(np.arctan2(y, x))

    return np.column_stack((r, theta_degrees))


def convert_3D_coords_to_2D_polar(coords_3d: np.ndarray, exclude_axis: int) -> np.ndarray:
    # Map axis to the remaining pair of coordinates
    axis_pairs = {0: (1, 2), 1: (0, 2), 2: (0, 1)}

    # Extract the appropriate coordinates based on the excluded axis
    x, y = coords_3d[:, axis_pairs[exclude_axis][0]], coords_3d[:, axis_pairs[exclude_axis][1]]

    # Pass to the to_2D_polar_coords function
    return to_2D_polar_coords(np.column_stack((x, y)))

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════