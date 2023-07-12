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

# INITIALIZE 
filename = r"Cropped Images\test13.png"
img = cv2.imread(filename)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
minPixelsForDefect = 20
defectCounter = 0

print("begin write")

# find image size and set unit length
h, w = img.shape[:2]
print(h, w)
unitLen = 40
unitWid = 40  # measures the pixel dimensions of one unit box
newLen = round(h/unitLen) # akin to rows
newWid = round(w/unitWid) # akin to cols


# draw grid
gridImg = img.copy()
gridImg = draw_grid(gridImg, grid_shape=(newLen, newWid), color=(255, 255, 255), thickness=1)

# set up progress indicators
progress = 0
progCounter = 0

# check each box for white pixels
for bigRows in range(newLen-1):
    for bigCols in range(newWid-1):
        count = 0
        for unitRow in range(unitLen):
            for unitCol in range(unitWid):
                k = img[unitRow+unitLen*(bigRows), unitCol+unitWid*(bigCols)]
                if k[0] > 100 and count > minPixelsForDefect:  # fill in the boxes where a white pixel is found
                    gridImg[bigRows*unitLen+1:(bigRows+1)*unitLen, bigCols*unitWid+1:(bigCols+1)*unitWid] = (0, 0, 255)
                    defectCounter += 1
                    break
                elif k[0] > 100: 
                    count += 1
    # show progress
    if (bigRows/(h/unitLen) * 100)> progCounter*20.0:
        progress = round(bigRows/(h/unitLen) * 100)
        print(str(progress) + r"% complete")
        progCounter += 1

cv2.imwrite("Sectored Images/pretest10.jpg", gridImg)
print("Number of defect points detected: " + str(defectCounter))
print("made using image at this path: " + filename)

print("write complete")
