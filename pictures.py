import cv2
import keyboard
import pyautogui
import time

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
