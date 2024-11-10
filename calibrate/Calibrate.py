# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    CALIBRATE/ PLOT LEDS                     CREATED: 2024-10-19          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Process -
# Take Pictures From All Angles -
#   - Give angle and update ANGLE_SET with all the different angles we used.
# Process Images -
#   - Find "bright" spot in each iamge and save that x, y coord into it's respective angle folder
#   - Do we care about average? Yes we need average so we can get it centered on x=0
#   - For "0" values we should output that list and have another program that lets us auto select those.
# Calculate Initial Coords -
#   - Read all processed iamge lists
#   - For each angle->angle set we have valid readings from calculate their 3D space. (Note can't do 180 degree)
#       - We can now 'average' this 3D coord if we have multiple good conversions, ie 0->90 and 90->180.
# Correct Coords
#   - Here we should do any rounding if it hasn't been done yet.
#   - Center x and z on 0. Make y floor at 0. ie shift so min val is 0.
#
# Profit?
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import cv2
import numpy as np
import keyboard
import pyautogui
import time
import math
from math import cos, sin

NUM_LEDS = 650
ANGLE_SET = [0, 90, 180, 270]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: For the given 'angle' it takes a picture of every single LED on our strip incrementing through another
             terminal using the "Enter" key.
INPUT: angle - which current angle we are taking pictures at to add to the correct folder/ name.
OUTPUT: Saves off all the pictures to their respective folders for the given angle.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def take_pictures(angle: int):
    cam_port = 1
    cam = cv2.VideoCapture(cam_port)
    pyautogui.click(1000, 1800)
    
    for count in range(0, NUM_LEDS):
        print(f"Taking Picture of LED {count}")
        result, image = cam.read()
        if result:
            cv2.imwrite(f"coords/{angle}/{angle}_{count}.png", image)
        else:
            print(f"No image detected. Start From LED {count}")
            return
            
        keyboard.send("enter")
        time.sleep(0.3)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Reads all of our images and does some basic computer vision to find where the LED is on the picture.
INPUT: Requires the pictures from 'take_pictures'.
OUTPUT: Coords txt files are saved with the given angle and pixel xy coords where the LED was seen.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def gen_auto_coordinates():
    sum_x = 0
    sum_y = 0
    leds_found = 0
    
    for theta in ANGLE_SET:
        file = open(f"coords/{theta}_auto.txt", 'w')
        
        for count in range(NUM_LEDS):
            img = cv2.imread(f"coords/{theta}/{theta}_{count}.png", 2)
            ret, bw_img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
            mass_y, mass_x = np.where(bw_img >= 255)
            
            if mass_x.size > 0 or mass_y.size > 0:
                x = round(np.average(mass_x))
                y = round(np.average(mass_y))
                file.write(f"{x} {y}\n")
                sum_x += x
                sum_y += y
                leds_found += 1
            else:
                file.write("0 0\n")
            
        file.close()
    
    average_x = sum_x / leds_found
    average_y = sum_y / leds_found
    print(average_x, average_y)

# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Takes the calculated coords from image processing and figures out where in 3D space they are.
INPUT: Requires all of the coords files from 'gen_auto_coordinates'.
OUTPUT: Writes to a text file 'auto_coordinates.txt' with all of our 3D coordiantes for the system. It defaults to 
        0, 0, 0 if it was unable to calculate properly.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def calc_auto_coords():
    file_0 = open("coords/0_auto.txt", 'r')
    file_90 = open("coords/90_auto.txt", 'r')
    file_180 = open("coords/180_auto.txt", 'r')
    file_270 = open("coords/270_auto.txt", 'r')

    file = open("coords/auto_coordinates.txt", 'w')

    degree_90 = math.pi / 2.0
    degree_180 = math.pi
    degree_270 = (3.0 * math.pi) / 2.0

    def rotate_x(coords, theta):
        return [coords[0], coords[1] * cos(theta) - coords[2]
                * sin(theta), coords[1] * sin(theta) + coords[2]
                * cos(theta)]

    def add_coords(coords_1, coords_2):
        return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1], coords_1[2] + coords_2[2]]

    # Gives [x, y, z] of coord_0
    def xy_x(coord_0, coord_1, theta):
        # We also average the x coordinate here since it might not be perfect
        return [(coord_0[0] + coord_1[0]) / 2.0, coord_0[1], (coord_0[1] * cos(theta) - coord_1[1]) / sin(theta)]

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

    print(average_x / final_count, average_y / final_count, average_z / final_count)

    file.close()
    file_0.close()
    file_90.close()
    file_180.close()
    file_270.close()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Just a simple adjuster so that we can center our coordiantes on 0, 0, 0. Requires us to update the offset
             values with the "average" value for each axis.
INPUT: Reads our auto_coordiantes.txt file to adjust coordiantes.
OUTPUT: Writes out to a new file the "corrected" coordinates.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def adjust_auto_coordinates():
    file = open("coords/auto_coordinates.txt", 'r')
    write_File = open("coords/auto_corrected_coordinates.txt", 'w')
    
    for x in range(NUM_LEDS):
        coord = file.readline().split()
        if coord[2] != '0':
            x_offset = 0
            y_offset = 0
            z_offset = 0
            
            write_File.write(f"{int(coord[0]) + x_offset} {int(coord[1]) + y_offset} {int(coord[2]) + z_offset}\n")
        else:
            write_File.write(f"{int(coord[0])} {int(coord[1])} {int(coord[2])}\n")
    file.close()
    write_File.close()


def main():
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    # GATHER DATA ═════════════════════════════════════════════════════════════════════════════════════════════════════
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    # take_pictures(0)
    # take_pictures(90)
    # take_pictures(180)
    # take_pictures(270)
    
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    # CALCULATE ═══════════════════════════════════════════════════════════════════════════════════════════════════════
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    # gen_auto_coordinates()
    # calc_auto_coords()
    # adjust_auto_coordinates()
    
    print("Done")
    
    
if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
