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

    # Rotation matrices
    R_x = np.array([[1, 0, 0]
                    , [0, np.cos(rx), -np.sin(rx)]
                    , [0, np.sin(rx), np.cos(rx)]])
    
    R_y = np.array([[np.cos(ry), 0, np.sin(ry)]
                    , [0, 1, 0]
                    , [-np.sin(ry), 0, np.cos(ry)]])
    
    R_z = np.array([[np.cos(rz), -np.sin(rz), 0]
                    , [np.sin(rz), np.cos(rz), 0]
                    , [0, 0, 1]])

    # Combined rotation matrix
    R = R_z @ R_y @ R_x
    return R @ point


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