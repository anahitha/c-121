import cv2
import time
import numpy as np

format = cv2.VideoWriter_fourcc(*"XVID")
file = cv2.VideoWriter("output.avi", format, 20.0, (640, 480))
capture = cv2.VideoCapture(0)
time.sleep(2)
bg = 0
for i in range(60):
    ret, bg = capture.read()
bg = np.flip(bg, axis = 1)
while (capture.isOpened()):
    ret, img = capture.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    u_black = np.array([104, 153, 70]) 
    l_black = np.array([30, 30, 0]) 
    mask1 = cv2.inRange(hsv, l_black, u_black)
    lowred = np.array([170, 120, 50])
    upred = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lowred, upred)
    mask1+=mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(img, img, mask = mask2)
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)
    fin = cv2.addWeighted(res1, 1, res2, 1, 0)
    file.write(fin)
    cv2.imshow("name", fin)
    cv2.waitKey(1)
capture.release()
file.release()
cv2.destroyAllWindows()