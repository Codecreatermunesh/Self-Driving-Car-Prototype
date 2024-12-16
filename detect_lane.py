#!/usr/bin/env python3.4
#OpenCV 3.1.0
import math
import cv2
import numpy as np
import time

#This Python script is designed for real-time video processing using OpenCV. It captures video from a webcam, processes 
#each frame to detect lines and then determine the direction of those lines (left, right, or straight) based on their angles






def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
    theta1 = math.atan(m)                  #calculate the slope angle
    return theta1*(180/np.pi)              #Calculated angle in radians


cap = cv2.VideoCapture(0)


a=b=c=1  #Initializes state variables a, b, and c to 1. These are used for controlling when direction changes are printed.

#Loops while the video capture is open
#cap.read() captures a frame, returning ret (boolean for success) and img (the image).
#Converts img to grayscale (gray) for simpler processing.
# Equalizes the histogram (equ) to improve contrast in low-light or high-contrast areas.
# Applies Gaussian blur (blur) to reduce noise and smooth the image.
# Applies a binary threshold (thresh) to highlight bright regions, setting values above 240 to white (255).
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img,(600,600))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(equ,(5,5),0)
    ret, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)


   	
    # Find Contours
	 #cv2.findContours detects the contours (outlines) of shapes in the thresholded image.
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw Contour
	#cv2.drawContours draws those contours on thresh in blue for visualization.
    cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)

    #Creates an empty black image of the same size as img for drawing purposes.
    drawing = np.zeros(img.shape, np.uint8)

	# Uses the Probabilistic Hough Line Transform to detect lines in the thresh image.
	# minLineLength sets the minimum length of a line to be detected.
	# maxLineGap allows for gaps in a single line segment.	
    lines = cv2.HoughLinesP(thresh, cv2.HOUGH_PROBABILISTIC, np.pi/180, 25, minLineLength = 10, maxLineGap = 40)


	
#For each detected line, calculates its slope using slope.
# Checks if the line is within a certain vertical range (250 < y < 600) to avoid false detection at the edges.
# Counts lines angled between -80 and -30 degrees as "right" (r) and between 30 and 80 degrees as "left" (l).
# Draws these lines in green on the original img using cv2.line.

    l=r=0
    for line in lines:
        
        for x1,y1,x2,y2 in line:
             if (round(x2-x1)!=0):
                  arctan = slope(x1,x2,y1,y2)
                  
                  if(y1>250 and y1<600 and y2>250 and y2<600):

                       if (round(arctan>=round(-80)) and round(arctan<=round(-30))):
                            r+=1
                            l=0
                            cv2.line(img,(x1, y1),(x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
                  
                       if ( round(arctan>=round(30)) and round(arctan<=round(80))):
                            l+=1
                            r=0
                            cv2.line(img,(x1, y1),(x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        
                  

    #Direction Determination:
    if l>=10 and a==1:
        
        print ('left')
	
        #time.sleep(0.3)
        a=0
        b=1
        c=1
    elif r>=10 and b==1:
        print ('right')
	
        #time.sleep(0.3)
        a=1
        b=0
        c=1
    elif l<10 and r<10 and c==1:
        print ('straight')
	
        a=1
        b=1
        c=0
    cv2.imshow('video', thresh) #Displays the processed frame (thresh) and the original frame with detected lines (img).
    cv2.imshow('video1', img)
    #cv2.imshow('equ', drawing)
    #cv2.imshow('edge', equ)
    if cv2.waitKey(1) & 0xFF == ord('q'): #Waits for 'q' key press to exit the loop.
        
        break

cap.release()
cv2.destroyAllWindows()
# Summary: This code captures video from a webcam, processes each frame to detect lines within a specific region, and then 
#determines if the lines indicate a "left", "right", or "straight" direction based on their slope. The detected direction is 
#printed to the console, and the lines are drawn on the video feed for visualization. The program continues running until the 
#user presses 'q' to quit.
