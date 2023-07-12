import numpy as np
import cv2

# CHANGABLE SETTINGS
imgOrg = cv2.imread('Processed Images\sky4.png')
radius = 2000 # measured in pixels
backgroundColor = (0,0,0) # black
backgroundColor = (255,255,255) # white

print("Loading crop")

# invert image colors to make the wafer white
img = cv2.bitwise_not(imgOrg)

# apply laplacian filter
kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
imgLaplacian = cv2.filter2D(img, cv2.CV_32F, kernel)
sharp = np.float32(img)
imgResult = sharp - imgLaplacian

imgResult = np.clip(imgResult, 0, 255)
imgResult = imgResult.astype('uint8')
imgLaplacian = np.clip(imgLaplacian, 0, 255)
imgLaplacian = np.uint8(imgLaplacian)

# create BW image
bw = cv2.cvtColor(imgResult, cv2.COLOR_BGR2GRAY)
_, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# apply image cleanup
kernel = np.ones((5, 5), np.uint8)
dilate = cv2.dilate(bw, kernel, iterations=3)

# apply distance transform
dist = cv2.distanceTransform(dilate, cv2.DIST_L2, 3)

# perform minmax to find center of transform
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(dist)
print(minVal, maxVal, minLoc, maxLoc)

# find radius and draw circle crop
mask = np.zeros(img.shape, dtype=np.uint8)
cv2.circle(mask, maxLoc, radius, (255,255,255),-1)

ROI = cv2.bitwise_and(imgOrg, mask)

# crop image
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
x,y,w,h = cv2.boundingRect(mask)
result = ROI[y:y+h, x:x+w]
mask = mask[y:y+h, x:x+w]
result[mask==0] = backgroundColor


cv2.imwrite("Cropped Images/test19.png", result)
print("Write complete")
