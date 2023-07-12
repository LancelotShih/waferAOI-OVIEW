import numpy as np
import cv2
import os
import argparse
import random as rng
import matplotlib.pyplot as plt


def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
    # we will use this to create our sectors
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = round(h / rows), round(w / cols)
    print("x values")
    # draw vertical lines
    for x in range(h):
        if x % dy == 0:
            cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    print("y values")
    # draw horizontal lines
    for y in range(w):
        if y % dx == 0:
            cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img


img = cv2.imread(r"Cropped Images\test12.png")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
minPixelsForDefect = 20
defectCounter = 0

print("begin write")

# find image size and set unit length
h, w = img.shape[:2]
print(h, w)
unitLen = round(h/64)
unitWid = round(w/64)  # measures the unit size we will be using for our boxes

# draw grid
gridImg = img.copy()
gridImg = draw_grid(gridImg, grid_shape=(64, 64),
                    color=(255, 255, 255), thickness=1)

# check each box for white pixels
for bigRows in range(63):
    for bigCols in range(63):
        count = 0
        for unitRow in range(60):
            for unitCol in range(60):
                k = img[unitRow+60*(bigRows), unitCol+60*(bigCols)]
                if k[0] > 100 and count > minPixelsForDefect:  # fill in the boxes where a white pixel is found
                    gridImg[bigRows*60+1:(bigRows+1)*60, bigCols*60+1:(bigCols+1)*60] = (0, 0, 255)
                    defectCounter += 1
                    break
                elif k[0] > 100: 
                    count += 1

cv2.imwrite("Sectored Images/pretest8.jpg", gridImg)
print("Number of defect points detected: " + str(defectCounter))

print("write complete")
