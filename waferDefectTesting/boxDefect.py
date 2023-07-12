import numpy as np
import cv2 
import os
import argparse
import random as rng
import matplotlib.pyplot as plt

img = cv2.imread("sky1-modified.png")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold = 100
# rows, cols, _ = img.shape

print("begin write")

# print(rows, cols)

# for i in range(rows):
#     for j in range(cols):
#         k = img[i,j]
#         if str(k) != "[0 0 0]": # we have hit a white spot on the wafer
#             # begin filtering for defects deemed high enough relevance
#             b = np.where(k > 100)
#             img[i,j]=[0,0,255]
#             print(k[b], i,j)

# for i in range(rows):
#     for j in range(cols):
#         k = img[i,j]
#         if str(k) != "[0 0 0]": # we have hit a white spot on the wafer
#             # check bottom neighbors for white spots 
#             # find height
#             mover = img[i,j]
#             imax = i
#             jmax = j
#             while True:
#                 if img[i+1,j] != "[0 0 0]":
#                     mover = img[i+1,j]
#                 elif img[i+1,j-1] != "[0 0 0]":
#                     mover = img[i+1,j-1]
#                 elif img[i,j-1] != "[0 0 0]":
#                     mover = img[i,j-1]
#                 elif img[i+1,j+1] != "[0,0,0]":
#                     mover = img[i+1,j]
#                 else:
#                     break # no more white spots to be found, corners of defect reached

# ####

# thresh = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # contours = contours[0] if len(contours) == 2 else contours[1]

# for i in contours:
#     x,y,w,h = cv2.boundingRect(i)
#     cv2.rectangle(img, (x,y), (x+w,y+h), color = (0,0,255), thickness = 2)

# cv2.imwrite("Bounded Images/test3.jpg", img)
# print("Number of defect points detected: " + str(len(contours)))

# print("write complete")

# ####

                ## ok theres a better way to do this, just use findcontours via edge detection


edges = cv2.Canny(imgGray, threshold, threshold*2)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

idx = 0
for i in range(len(contours)):
    # contouredImage = cv2.drawContours(imgGray, contours[i], -1,255,3)
    # c = max(contours[i],key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(contours[i])
    cv2.rectangle(img, (x,y), (x+w,y+h), color = (0,0,255), thickness = 1)

# cv2.imwrite("Bounded Images/test16.jpg", img)
print("Number of defect points detected: " + str(len(contours)))

print("write complete")