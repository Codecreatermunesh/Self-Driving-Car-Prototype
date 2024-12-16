# This code is designed to control a robot using an ultrasonic sensor to detect obstacles and GPIO pins to control motors 
# for movement. The robot/car(my case) moves forward until it detects an obstacle within a certain range, then changes direction 
# (left or right, backward and forward) to avoid the obstacle. Let's break it down in detail.

import RPi.GPIO as GPIO                    #Import GPIO library
import time

GPIO.setwarnings(False)          # Disable warnings about GPIO pins already being in use
GPIO.setmode(GPIO.BCM)           # Use BCM pin numbering for GPIO references

#TRIG and ECHO: These control the ultrasonic sensor. TRIG sends an ultrasonic pulse, and ECHO measures the time taken for 
#the pulse to return after hitting an obstacle.
TRIG = 17                        # Pin connected to the ultrasonic sensor's TRIG
ECHO = 27                        # Pin connected to the ultrasonic sensor's ECHO
led = 22                         # Pin connected to an LED indicator

#m11, m12, m21, m22 These pins Control the direction of two motors (left and right) by activating specific pin combinations.
m11 = 16                         # Pins connected to motor 1 (left wheel)
m12 = 12
m21 = 21                         # Pins connected to motor 2 (right wheel)
m22 = 20


GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
GPIO.setup(led,GPIO.OUT)                  

GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

GPIO.output(led, 1)

#time.sleep(5)

def stop():
    print ('stop')
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 0)          # Left motor backward pin is low
    GPIO.output(m12, 1)          # Left motor forward pin is high
    GPIO.output(m21, 1)          # Right motor forward pin is high
    GPIO.output(m22, 0)          # Right motor backward pin is low
    print('Forward')


def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print ('back')

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print ('left')

def right():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print ("right")

#stop()
count=0 ## Counter for determining direction (left/right)
while True:
 i=0
 avgDistance=0
 for i in range(5):
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  time.sleep(0.1)                                   #Delay

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                           #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
       GPIO.output(led, False)             
  pulse_start = time.time()

  while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
       GPIO.output(led, False) 
  pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor
  #print("pulse duration: ",pulse_duration)
  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
  distance = round(distance,2)                 #Round to two decimal points
  avgDistance=avgDistance+distance

 avgDistance=avgDistance/5
 print (avgDistance)
 flag=0
    #If an obstacle is detected within 100 cm, Alternate between turning left and right to avoid it.
 if avgDistance < 100:
    #Check whether the distance is within 100cm range
    count=count+1
    stop()
    time.sleep(1)
    #back()
    time.sleep(1.5)
    if (count%3 ==1) & (flag==0):
     right()
     flag=1
    else:
     left()
     flag=0
    time.sleep(1.5)
    stop()
    time.sleep(1)
 else:
    forward()
    flag=0
