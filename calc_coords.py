import math

file_0 = open("0.txt", "r")
file_90 = open("90.txt", "r")
file_180 = open("180.txt", "r")
file_270 = open("270.txt", "r")

file = open(f'coordinates.txt', 'w')

degree_0 = 0
degree_90 = math.pi/2.0
degree_180 = math.pi
degree_270 = (3.0*math.pi)/2

def rotate_x(coords, theta):
    resulting_coords = [coords[0], 0, 0]
    resulting_coords[1] = coords[1]*math.cos(theta) - coords[2]*math.sin(theta)
    resulting_coords[2] = coords[1]*math.sin(theta) + coords[2]*math.cos(theta)
    return resulting_coords

def add_coords(coords_1, coords_2):
    result_coords = [0, 0, 0]
    result_coords[0] = coords_1[0] + coords_2[0]
    result_coords[1] = coords_1[1] + coords_2[1]
    result_coords[2] = coords_1[2] + coords_2[2]
    return result_coords

count = 0
for x in range(0, 350):
    coord_0 = file_0.readline().split()
    coord_90 = file_90.readline().split()
    coord_180 = file_180.readline().split()
    coord_270 = file_270.readline().split()
    
    final_coords = [0, 0, 0]
    final_coords_0 = [0, 0, 0]
    final_coords_90 = [0, 0, 0]
    final_coords_180 = [0, 0, 0]
    final_coords_270 = [0, 0, 0]
    count = 0.0
    final_count = 0.0

    if coord_0 != ['0', '0']:
        final_coords_0[0] = float(coord_0[0])
        final_coords_0[1] = float(coord_0[1]) - 320
        if coord_90 == ['0', '0']:
            final_coords_0[2] += float(coord_90[0])*math.sin(degree_270) + (float(coord_90[1])-320)*math.sin(degree_270)
            count += 1.0
        if coord_180 == ['0', '0']:
            final_coords_0[2] += float(coord_180[0])*math.sin(degree_180) + (float(coord_180[1])-320)*math.sin(degree_180)
            count += 1.0
        if coord_270 == ['0', '0']:
            final_coords_0[2] += float(coord_270[0])*math.sin(degree_90) + (float(coord_270[1])-320)*math.sin(degree_90)
            count += 1.0
        if count != 0.0:
            final_coords = add_coords(final_coords, final_coords_0)
            final_coords_0[2] = final_coords_0[2] / count
            final_count += 1.0
        else:
            final_coords_0[0] = 0
            final_coords_0[1] = 0
        count = 0.0

    if coord_90 != ['0', '0']:
        final_coords_90[0] = float(coord_90[0]) # TODO: FIX
        final_coords_90[1] = float(coord_90[1]) - 320 # TODO: FIX
        if coord_0 == ['0', '0']:
            final_coords_90[2] += float(coord_0[0])*math.sin(degree_90) + (float(coord_0[1])-320)*math.sin(degree_90)
            count += 1.0
        if coord_180 == ['0', '0']:
            final_coords_90[2] += float(coord_180[0])*math.sin(degree_270) + (float(coord_180[1])-320)*math.sin(degree_270)
            count += 1.0
        if coord_270 == ['0', '0']:
            final_coords_90[2] += float(coord_270[0])*math.sin(degree_180) + (float(coord_270[1])-320)*math.sin(degree_180)
            count += 1.0
        if count != 0.0:
            final_coords_90[2] = final_coords_90[2] / count
            final_coords = add_coords(final_coords, rotate_x(final_coords_90, degree_270))
            final_count += 1.0
        else:
            final_coords_90[0] = 0
            final_coords_90[1] = 0
        count = 0.0
        # Gotta rotate back to to 0
    
    if coord_180 != ['0', '0']:
        final_coords_180[0] = float(coord_180[0]) # TODO: FIX
        final_coords_180[1] = float(coord_180[1]) - 320 # TODO: FIX
        if coord_0 == ['0', '0']:
            final_coords_180[2] += float(coord_0[0])*math.sin(degree_180) + (float(coord_0[1])-320)*math.sin(degree_180)
            count += 1.0
        if coord_90 == ['0', '0']:
            final_coords_180[2] += float(coord_90[0])*math.sin(degree_90) + (float(coord_90[1])-320)*math.sin(degree_90)
            count += 1.0
        if coord_270 == ['0', '0']:
            final_coords_180[2] += float(coord_270[0])*math.sin(degree_270) + (float(coord_270[1])-320)*math.sin(degree_270)
            count += 1.0
        if count != 0.0:
            final_coords_180[2] = final_coords_180[2] / count
            final_coords = add_coords(final_coords, rotate_x(final_coords_180, degree_180))
            final_count += 1.0
        else:
            final_coords_180[0] = 0
            final_coords_180[1] = 0
        count = 0.0
        # Gotta rotate back to to 0

    if coord_270 != ['0', '0']:
        final_coords_270[0] = float(coord_270[0])
        final_coords_270[1] = float(coord_270[1]) - 320
        if coord_0 == ['0', '0']:
            final_coords_270[2] += float(coord_0[0])*math.sin(degree_270) + (float(coord_0[1])-320)*math.sin(degree_270)
            count += 1.0
        if coord_90 == ['0', '0']:
            final_coords_270[2] += float(coord_90[0])*math.sin(degree_180) + (float(coord_90[1])-320)*math.sin(degree_180)
            count += 1.0
        if coord_180 == ['0', '0']:
            final_coords_270[2] += float(coord_180[0])*math.sin(degree_90) + (float(coord_180[1])-320)*math.sin(degree_90)
            count += 1.0
        if count != 0.0:
            final_coords_270[2] = final_coords_270[2] / count
            final_coords = add_coords(final_coords, rotate_x(final_coords_270, degree_90))
            final_count += 1.0
        else:
            final_coords_270[0] = 0
            final_coords_270[1] = 0
        count = 0.0
        # Gotta rotate back to to 0

    if final_count != 0:
        final_coords[0] = final_coords[0] / final_count
        final_coords[1] = final_coords[1] / final_count
        final_coords[1] = final_coords[2] / final_count
    file.write(f"{int(final_coords[0])} {int(final_coords[1])} {int(final_coords[2])}\n")
file.close()
file_0.close()
file_90.close()
file_180.close()
file_270.close()