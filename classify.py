import socket
import time
import cv2
import numpy as np
import threading

global img
def classifyGR():
    green = np.uint8([[[0, 255, 0]]])  #green color
    hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV) #hsv value of green color 
    print(hsvGreen) 
    
    lowerLimit = hsvGreen[0][0][0] - 10, 100, 100  # range of green color lower limit and upper limit
    upperLimit = hsvGreen[0][0][0] + 10, 255, 255
    
    print(upperLimit)
    print(lowerLimit)
    
    red = np.uint8([[[0, 0, 255]]]) #red color
    hsvred = cv2.cvtColor(red, cv2.COLOR_BGR2HSV) #hsv value of red color
    print(hsvred)
    
    lower = hsvred[0][0][0] - 10, 100, 100 # range of red color lower limit and upper limit
    upper = hsvred[0][0][0] + 10, 255, 255
    
    print(upper)
    print(lower)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert the image into hsv
    
    lg = np.array(lowerLimit) #range of green color
    ug = np.array(upperLimit)
    
    green_mask = cv2.inRange(hsv, lg, ug) #green masked image
    cv2.imshow('green', green_mask) #show the image 
    
    lr = np.array(lower) #range of red color
    ur = np.array(upper)
    
    red_mask = cv2.inRange(hsv, lr, ur) #red masked image
    cv2.imshow('red', red_mask)  #show the image
    global timer
    timer = threading.Timer(0.5, classifyGR())
    timer.start()

tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)
mypc_address = ('192.168.10.2', 12345)
socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
socket.bind (mypc_address)
socket.sendto ('command'.encode (' utf-8 '), tello_address)
socket.sendto ('streamon'.encode (' utf-8 '), tello_address)
print ("Start streaming")
capture = cv2.VideoCapture ('udp://0.0.0.0:11111',cv2.CAP_FFMPEG)
if not capture.isOpened():
    capture.open('udp://0.0.0.0:11111')

ret, frame = capture.read()
img = frame
timer = threading.Timer(0.5, classifyGR())
print(timer)
timer.start()
while True:
    ret, frame = capture.read()
    img = frame
    
    if(ret):
        cv2.imshow('frame', frame)
        
    if cv2.waitKey (1)&0xFF == ord ('q'):
        break
capture.release ()
cv2.destroyAllWindows ()
socket.sendto ('streamoff'.encode (' utf-8 '), tello_address)
