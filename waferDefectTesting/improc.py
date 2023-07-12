import numpy as np
import cv2
import os

imgSky = os.listdir(r"SiC\SKY")
imgPlate = os.listdir(r"SiC\plate")
template = cv2.imread(r"sky1-modified.png")



count = 0

for i in imgSky:
    img =cv2.imread(r"SiC\SKY\\" + i)
    img = cv2.resize(img, (0,0), fx = 1, fy = 1.12) # 4385 x 3913 pixels originally for plate || 12% margin between two areas
    # img = cv2.resize(img, (0,0), fx = 0.1, fy = 0.1) # if you want to see your image
    h, w = i.shape


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    (T, circleImg) = cv2.threshold(blurred,130,255, cv2.THRESH_BINARY)
    cv2.imshow("detected?", circleImg)
    masked = cv2.bitwise_and(img, img, mask = circleImg)
    cv2.imshow("clipped", masked)
    status = cv2.imwrite("Processed Images\sky" + str(count) + ".png", masked)
    print("written to disk: ", status)

# begin template matching
    print("Finding label...")
    img2 = gray.copy()
    result = cv2.matchTemplate(img2, template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(cv2.minMaxLoc(result))
    # location = max_loc
    # bottomRight = (location[0] + w, location[1] + h)
    # print(location)
    # cv2.circle(img2, location, bottomRight, 255, 5)
    # cv2.imshow('Match', img2)
    # img2 = img2[location[1]: location[1] + h , location[0]: location[0] + w]
    # cv2.rectangle(img2, location, bottomRight, 255, 5)
    # cv2.imshow('Match', img2)
    # cv2.imwrite(r"processedCupImages\badCrop\bCrop" + str(count) + ".png", img2)

    count+=1
    cv2.waitKey(0)