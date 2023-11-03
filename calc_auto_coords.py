import math
from math import cos, sin 

file_0 = open("0_auto.txt", "r")
file_90 = open("90_auto.txt", "r")
file_180 = open("180_auto.txt", "r")
file_270 = open("270_auto.txt", "r")

file = open(f'auto_coordinates.txt', 'w')

degree_0 = 0
degree_90 = math.pi/2.0
degree_180 = math.pi
degree_270 = (3.0*math.pi)/2.0

def rotate_x(coords, theta):
    return [coords[0], coords[1]*cos(theta) - coords[2]*sin(theta), coords[1]*sin(theta) + coords[2]*cos(theta)]

def add_coords(coords_1, coords_2):
    return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1], coords_1[2] + coords_2[2]]

# Gives [x, y, z] of coord_0
def xy_x(coord_0, coord_1, theta):
    # We also average the x coordinate here since it might not be perfect
    return [(coord_0[0] + coord_1[0])/2.0, coord_0[1], (coord_0[1]*cos(theta) - coord_1[1]) / sin(theta)]

final_count = 0.0
average_x = 0.0
average_y = 0.0
average_z = 0.0

for x in range(0, 350):
    coord_0 = file_0.readline().split()
    coord_90 = file_90.readline().split()
    coord_180 = file_180.readline().split()
    coord_270 = file_270.readline().split()
    
    final_coord = [0, 0, 0]
    # Float Casting and adjusting y axis to best get center of tree on x-axis
    y_axis_shift = 256.0

    coord_0 = [float(coord_0[0]), (float(coord_0[1]) - y_axis_shift)]
    coord_90 = [float(coord_90[0]), (float(coord_90[1]) - y_axis_shift)]
    coord_180 = [float(coord_180[0]), (float(coord_180[1]) - y_axis_shift)]
    coord_270 = [float(coord_270[0]), (float(coord_270[1]) - y_axis_shift)]

    count = 0.0
    # 0 -> 90
    if coord_0[0] != 0.0 and coord_90[0] != 0.0:
        final_coord = add_coords(final_coord, xy_x(coord_0, coord_90, degree_90))
        count += 1.0
    
    # 90 -> 180
    if coord_90[0] != 0.0 and coord_180[0] != 0.0:
        final_coord = add_coords(final_coord, rotate_x(xy_x(coord_90, coord_180, degree_90), degree_270))
        count += 1.0

    # 180 -> 270
    if coord_180[0] != 0.0 and coord_270[0] != 0.0:
        final_coord = add_coords(final_coord, rotate_x(xy_x(coord_180, coord_270, degree_90), degree_180))
        count += 1.0

    # 270 -> 0
    if coord_270[0] != 0.0 and coord_0[0] != 0.0:
        final_coord = add_coords(final_coord, rotate_x(xy_x(coord_270, coord_0, degree_90), degree_90))
        count += 1.0
    
    if count != 0.0:
        final_coord[0] = round(final_coord[0] / count)
        final_coord[1] = round(final_coord[1] / count)
        final_coord[2] = round(final_coord[2] / count)
        final_count += 1.0
        average_x += final_coord[0]
        average_y += final_coord[1]
        average_z += final_coord[2]
        
    file.write(f"{final_coord[0]} {final_coord[1]} {final_coord[2]}\n")

print(average_x/final_count, average_y/final_count, average_z/final_count)

file.close()
file_0.close()
file_90.close()
file_180.close()
file_270.close()