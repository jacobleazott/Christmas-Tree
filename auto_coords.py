import cv2
import numpy as np
import keyboard
import pyautogui
import time

def take_picture():
    cam_port = 1
    cam = cv2.VideoCapture(cam_port)
    limit = 350

    count = 0
    pyautogui.click(1000,1800)
    while True:
        print(f"Take Picture of LED {count}")
        result, image = cam.read()
        if result:
            cv2.imwrite(f"270/270_{count}.png", image)
        else:
            print("No image detected. Please! try again")
        count += 1
        keyboard.send("enter")
        time.sleep(0.3)

        if count == limit:
            break

def gen_auto_coordinates():
    average_y = 0
    average_x = 0
    count = 0
    for theta in (0, 90, 180, 270):
        file = open(f'{theta}_auto.txt', 'w')
        for i in range(0, 350):
            img = cv2.imread(f'{theta}/{theta}_{i}.png', 2)
            ret, bw_img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)
            mass_y, mass_x = np.where(bw_img >= 255)
            if mass_x.size > 0 or mass_y.size > 0:
                x = round(np.average(mass_x))
                y = round(np.average(mass_y))
                file.write(f"{x} {y}\n")
                average_x += x
                average_y += y
                count += 1
            else:
                file.write(f"0 0\n")
        file.close()
    average_x = average_x / count
    average_y = average_y / count
    # 339 256
    print(average_x, average_y)
    
def adjust_auto_coordinates():
    file = open(f'auto_coordinates.txt', 'r')
    write_File = open(f'auto_corrected_coordinates.txt', 'w')
    
    for x in range(0, 350):
        coord = file.readline().split()
        if coord[2] != '0':
            write_File.write(f"{int(coord[0]) - 350} {int(coord[1]) + 1} {int(coord[2]) + 13}\n")
        else:
            write_File.write(f"{int(coord[0])} {int(coord[1])} {int(coord[2])}\n")
    file.close()
    write_File.close()

adjust_auto_coordinates()