# importing cv2
import cv2
import numpy as np
   
# path
path = '0/0_349.png'

theta = 0

for i in range(0, 350):
    img = cv2.imread(f'{theta}/{theta}_{i}.png', 2)
    image = cv2.imread(f'{theta}/{theta}_{i}.png')
    ret, bw_img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    mass_y, mass_x = np.where(bw_img >= 255)
    if mass_x.size > 0 or mass_y.size > 0:
        center = round(np.average(mass_x)), round(np.average(mass_y))
        print(center)
        circ = cv2.circle(image, center, 30, (0, 0, 255), 1)
        cv2.imshow("test", circ)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
