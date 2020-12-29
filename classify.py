import socket
import time
import cv2
import numpy as np
import threading

### golbal var ###
counter = 0

# color var 
green = np.uint8([[[0, 255, 0]]])  #green color
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV) #hsv value of green color 

lowerLimitGreen = hsvGreen[0][0][0] - 10, 100, 100  # range of green color lower limit and upper limit
upperLimitGrenn = hsvGreen[0][0][0] + 10, 255, 255

#range of green color
lg = np.array(lowerLimit) 
ug = np.array(upperLimit)

red = np.uint8([[[0, 0, 255]]]) #red color
hsvRed = cv2.cvtColor(red, cv2.COLOR_BGR2HSV) #hsv value of red color

lowerLimitRed = hsvred[0][0][0] - 10, 100, 100 # range of red color lower limit and upper limit
upperLimitRed = hsvred[0][0][0] + 10, 255, 255

#range of red color
lr = np.array(lower) 
ur = np.array(upper)


def classifyGR():
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert the image into hsv

    green_mask = cv2.inRange(hsv, lg, ug) #green masked image
    cv2.imshow('green', green_mask) #show the image 
    
    red_mask = cv2.inRange(hsv, lr, ur) #red masked image
    cv2.imshow('red', red_mask)  #show the image
    
if __name__ == '__main__':
    # tello set up
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

    while True:
        ret, frame = capture.read()
        if(counter%10==0):
            if(ret):
                cv2.imshow('frame', frame)

            if(cv2.waitKey(1)&0xFF == ord ('q')):
                break
            counter++
    
    capture.release ()
    cv2.destroyAllWindows ()
    socket.sendto ('streamoff'.encode (' utf-8 '), tello_address)
