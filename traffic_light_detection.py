import cv2  # OpenCV library
import numpy as np
import RPi.GPIO as GPIO
import time

# Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 17
ECHO = 27
led = 22

m11 = 16
m12 = 12
m21 = 21
m22 = 20

GPIO.setup(TRIG, GPIO.OUT)  # Initialize GPIO Pin as outputs
GPIO.setup(ECHO, GPIO.IN)  # Initialize GPIO Pin as input
GPIO.setup(led, GPIO.OUT)

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

def stop():
    print('stop')
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Start')

# Capturing video through webcam
cap = cv2.VideoCapture(0)   #Opens the default camera (ID 0) for capturing video frames.

# Set the window name and initial size
cv2.namedWindow("Color Tracking", cv2.WINDOW_NORMAL)  #Creates a resizable window named Color Tracking for the video feed.
cv2.resizeWindow("Color Tracking", 1280, 720)  # Adjust the size as needed

forward()  #The robot(car) starts moving forward initially.


# cap.isOpened(): Ensures the camera is active before capturing frames.
# cap.read(): Captures a frame from the video feed.
# img1[30:2000, 500:700]: Crops the frame to focus on a specific region of interest (height: 30–2000 pixels, width: 500–700 pixels). 
# This reduces processing load and focuses on relevant areas.
while cap.isOpened():
    _, img1 = cap.read()
    img = img1[30:2000, 500:700]

    # Converting frame (BGR) to HSV (hue-saturation-value), which is more effective for color detection.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of red color
    red_lower = np.array([136, 87, 111], np.uint8)  #np.uint8 specifies the data type of the NumPy array as unsigned 8-bit integers.
    red_upper = np.array([180, 255, 255], np.uint8) #This is commonly used in image processing because most image data (like pixel intensity values in RGB or HSV) is represented as 8-bit unsigned integers.
     #HSV Values([136,87,111]).
    #HSV stands for Hue, Saturation, and Value. It is a color model used in image processing and computer vision to represent 
    #colors in a way that is more intuitive than the traditional RGB (Red, Green, Blue) model.
    # Define the range of green color (you may need to adjust these values)
    green_lower = np.array([35, 80, 80], np.uint8)
    green_upper = np.array([85, 255, 255], np.uint8)

    # Find the range of red and green color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)

    # Morphological transformation, Dilation
    kernel = np.ones((5, 5), "uint8")
    red = cv2.dilate(red, kernel)
    green = cv2.dilate(green, kernel)

    # Tracking the Red Color
    (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #red colour logic(using paper refrence)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "RED color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            print('Red')
            stop()

    # Tracking the Green Color
    (contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #green color code logic(using research paper reference that time)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Green color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
            print('Green')
            forward()

    cv2.imshow("Color Tracking", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()

