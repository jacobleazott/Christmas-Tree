import math
import cv2
import keyboard
from PIL import Image
import time
import pyautogui

theta = 270
file = open(f'{theta}.txt', 'w')

for i in range(0, 350):
    img = cv2.imread(f'{theta}/{theta}_{i}.png')
    cv2.imshow('image', img)
    cv2.waitKey()
    val = pyautogui.position()
    file.write(f"{val.x} {val.y}\n")
file.close()


