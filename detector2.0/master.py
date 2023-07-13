import numpy as np
import cv2
import os

# INITIALIZE
radius = 2000 # measured in pixels
backgroundColor = (0,0,0) # black
# backgroundColor = (255,255,255) # white
source = r"detector2.0/source"


imgSky = os.listdir(source)
count = 0
for i in imgSky:
    print("Processing image: " + str(i))
    print("Source path: " + source + str(i))
    print("")

    img =cv2.imread(r"detector2.0/source/" + i)
    img = cv2.resize(img, (0,0), fx = 1, fy = 1.12) # 4385 x 3913 pixels originally for plate || 12% margin between two areas

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    (T, circleImg) = cv2.threshold(blurred,130,255, cv2.THRESH_BINARY)
    resized = cv2.bitwise_and(img, img, mask = circleImg)
    print("Finished resizing")
    print("")
    print("Loading crop")
    # invert image colors to make the wafer white
    img = cv2.bitwise_not(resized)

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
    print("Raw image size: " + str(img.shape))
    print("Center found at: " + str(maxLoc))

    # find radius and draw circle crop
    mask = np.zeros(img.shape, dtype=np.uint8)
    cv2.circle(mask, maxLoc, radius, (255,255,255),-1)

    ROI = cv2.bitwise_and(resized, mask)

    # crop image
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    x,y,w,h = cv2.boundingRect(mask)
    result = ROI[y:y+h, x:x+w]
    mask = mask[y:y+h, x:x+w]
    result[mask==0] = backgroundColor

    img = result.copy()
    print("Cropped image size: " + str(img.shape))
    print("Crop complete")
    print("")

    # create bounding box image
    print("Begin bounding box detection")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = 100
    edges = cv2.Canny(imgGray, threshold, threshold*2)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for a in range(len(contours)):
        x,y,w,h = cv2.boundingRect(contours[a])
        cv2.rectangle(img, (x,y), (x+w,y+h), color = (0,0,255), thickness = 1)

    cv2.imwrite(r"detector2.0/bounded2.0/bounded" + str(i) + ".png", img)
    print("Number of defect points detected: " + str(len(contours)))
    print("Bounded image write complete")
    print("Output Path: detector2.0/bounded2.0/bounded" + str(i) + ".png")
    print("")

    # create sector chunk image
    print("Begin sector chunk detection")

    # INITIALIZE FOR SECTOR CHUNKING
    img = result
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    minPixelsForDefect = 5
    
    def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
        # we will use this to create our sectors
        h, w, _ = img.shape
        rows, cols = grid_shape
        dy, dx = round(h / rows), round(w / cols)
        # draw vertical lines
        for x in range(h):
            if x % dy == 0:
                cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

        # draw horizontal lines
        for y in range(w):
            if y % dx == 0:
                cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

        return img

    # find image size and set unit length
    h, w = img.shape[:2]
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
                        break
                    elif k[0] > 100: 
                        count += 1
        # show progress
        if (bigRows/(h/unitLen) * 100)> progCounter*20.0:
            progress = round(bigRows/(h/unitLen) * 100)
            print(str(progress) + r"% complete")
            progCounter += 1
    print(r"100% complete")
    print("")

    cv2.imwrite("detector2.0/sectored2.0/sectored" + str(i) + ".png", gridImg)
    print("Output Path: detector2.0/sectored2.0/sectored" + str(i) + ".png")
    print("--------------------")
    print("")

print("Write complete, files under paths: ")
print(r"detector2.0\bounded2.0")
print(r"detector2.0\sectored2.0")
print("")
print("Please transfer outputs from folders to elsewhere to avoid accidental data loss")
print("")
print("-----------------------")
print("")