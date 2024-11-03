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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes a givne list of cartesian 'coords' and converts them into polar coords ignoring the given 'axis'.
INPUT: coords - XYZ values of our cartestion coordinates we will be converting.
OUTPUT: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def to_2D_polar_coords(coords: tuple[Real, Real, Real], axis: int = 0) -> list[tuple[Real, Real]]:
    # Map the axis to the indices of the coordinates to keep
    axes = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    polar_coords = []
    
    for coord in coords:
        u, v = coord[axes[axis][0]], coord[axes[axis][1]]  # Extract u and v based on the ignored axis
        # Convert (u, v) to polar coordinates
        r = math.sqrt(u**2 + v**2)
        theta = math.atan2(v, u)  # Angle in radians
        theta_degrees = math.degrees(theta)  # Convert angle to degrees
        polar_coords.append((r, theta_degrees))

    return polar_coords

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════