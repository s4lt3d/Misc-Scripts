# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Walter
"""

import pandas as pd
import cv2
import time
cam = cv2.VideoCapture(1)   # 0 -> index of camera


start_time = time.time()
s, img_start = cam.read()

while time.time() - start_time < 30:
    print(".", end = "")
    time.sleep(1)

s, img_end = cam.read()

cv2.imshow('start', img_start)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('end', img_end)
cv2.waitKey(0)
cv2.destroyAllWindows()
