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
import numpy as np

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Given an array of XYZ points, rotate it around the origin with XYZ parts of 'angles'
INPUT: coords - Array of XYZ points we will be rotating.
       angles - XYZ rotation degrees we will apply to our 'coords'.
OUTPUT: Rotated XYZ coordiantes.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def rotate_coordinates(coords: np.ndarray, angles: np.ndarray) -> np.ndarray:
    theta_x, theta_y, theta_z = angles
    
    # Rotation matrices
    rx = np.array([
          [1, 0, 0]
        , [0, np.cos(theta_x), -np.sin(theta_x)]
        , [0, np.sin(theta_x), np.cos(theta_x)]])
    
    ry = np.array([
          [np.cos(theta_y), 0, np.sin(theta_y)]
        , [0, 1, 0]
        , [-np.sin(theta_y), 0, np.cos(theta_y)]])
    
    rz = np.array([
          [np.cos(theta_z), -np.sin(theta_z), 0]
        , [np.sin(theta_z), np.cos(theta_z), 0]
        , [0, 0, 1]])
    
    # Combined rotation matrix
    rot_matrix = rz @ ry @ rx  # Matrix multiplication in the correct order
    
    # Apply rotation to each coordinate (coords is shape (n, 3), R is 3x3)
    return np.dot(coords, rot_matrix.T)  # Dot product for each coordinate


def rotate_2d_coords(coords: np.ndarray, angle: float) -> np.ndarray:
    angle_rad = np.deg2rad(angle)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])

    return np.dot(coords, rotation_matrix.T)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes an array of 2D cartesian 'coords' and converts them into polar coords.
INPUT: coords - XY values of our cartestion coordinates we will be converting.
OUTPUT: Np array of 2D polar coords.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def to_2d_polar_coords(coords: np.ndarray) -> np.ndarray:
    x, y = coords[:, 0], coords[:, 1]
    r = np.hypot(x, y)  # Equivalent to sqrt(x**2 + y**2), more efficient
    theta_degrees = np.degrees(np.arctan2(y, x))
    
    return np.column_stack((r, theta_degrees))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes a givne list of 3D cartesian 'coords' and converts them into polar coords ignoring the given 'axis'.
INPUT: coords - XYZ values of our cartestion coordinates we will be converting.
OUTPUT: Np array of 2D polar coords created from the two axis selected.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def convert_3d_coords_to_2d_polar(coords_3d: np.ndarray, exclude_axis: int) -> np.ndarray:
    # Map axis to the remaining pair of coordinates and extract the appropriate coordinates based on the excluded axis.
    axis_pairs = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    first_axis, second_axis = coords_3d[:, axis_pairs[exclude_axis][0]], coords_3d[:, axis_pairs[exclude_axis][1]]
    
    return to_2d_polar_coords(np.column_stack((first_axis, second_axis)))


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
