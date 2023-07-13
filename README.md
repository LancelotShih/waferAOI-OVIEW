# waferAOI-OVIEW

This document details the use of the waferDefectTesting folder containing any original files used as a part of the detector2.0 master.py program

All files should be executed in the order that they are listed in below

For more process documentation, refer to this document here:
https://docs.google.com/document/d/1RRp9nG_6WpUpE1H-gimXqm5Y62kC3a5L975hIJNbR1I/edit?usp=sharing 

-------------------------------------------

Format:

filename
    purpose

-------------------------------------------

improc.py
    Takes a source image and resizes it into the correct aspect ratio akin to real conditions. The changable value is the 2nd line under the for loop

        img = cv2.resize(img, (0,0), fx = 1, fy = 1.12)

    Changing the fx and fy values accordingly will help resize the image according to the settings determined by the source image. The current source images have a 12% offset between the y and x axis. 

improc2.py
    Takes the image outputted by improc.py and cuts/crops it into a circle format such that all outer edges that are not the wafer are removed. 
    Changeable values include:
        - input image (should be the output from improc.py)
        - radius of the circle crop (default is set to 2000 pixels for our standards)
        - background color (human use recommends white background, computer use recommends black background)

boxDefect.py
    Takes the image outputted by improc2.py and draws bounding boxes around clusters of pixel defects. 
    Changeable values include:
        - input image (should be the output from improc2.py)
        - threshold (currently set at 100 but can be increased to up to 700)
        - output path (change the number at the end of the test to generate a new image else the old image will be overridden)
    
    Note: 
        Ignore the giant commented out section, it was brainstorming

sectorDefects2.py
    Successor of sectorDefects.py and NOT the second step. Takes the image outputted by improc2.py and creates a grid of 40x40 pixel unit squares (100x100 grid for our 4000x4000 images) and labels squares with defects inside of them with a red square. 
    Changeable values include:
        - input image (should be the output from improc2.py)
        - minPixelsForDefect is the minimum number of white pixels in a 40x40 unit box necessary for a defect to be deemed detected and marked with a red square
        - output path (change the number at the end of the test to generate a new image else the old image will be overridden)

    Note:
        sectorDefects.py DOES NOT FUNCTION PROPERLY ANYMORE, stick to sectorDefects2.py and edit this one accordingly. 