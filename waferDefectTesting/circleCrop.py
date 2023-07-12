import numpy as np
import cv2
import os

# Create mask and draw circle onto mask
image = cv2.imread('Processed Images/sky0.png')
mask = np.zeros(image.shape, dtype=np.uint8)
x,y = 335, 245
cv2.circle(mask, (x,y), 110, (255,255,255), -1)

# Bitwise-and for ROI
ROI = cv2.bitwise_and(image, mask)

# Crop mask and turn background white
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
x,y,w,h = cv2.boundingRect(mask)
result = ROI[y:y+h,x:x+w]
mask = mask[y:y+h,x:x+w]
result[mask==0] = (255,255,255)

cv2.imshow('result', result)
cv2.waitKey()