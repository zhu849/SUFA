import socket
import cv2
import numpy as np

green = np.uint8([[[0, 255, 0]]])  #green color
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV) #hsv value of green color 
red = np.uint8([[[0, 0, 255]]]) #red color
hsvred = cv2.cvtColor(red, cv2.COLOR_BGR2HSV) #hsv value of red color

lowerLimitGreen = hsvGreen[0][0][0] - 10, 100, 100  # range of green color lower limit and upper limit
upperLimitGreen = hsvGreen[0][0][0] + 10, 255, 255
lowerLimitRed = hsvred[0][0][0] - 10, 100, 100 # range of red color lower limit and upper limit
upperLimitRed = hsvred[0][0][0] + 10, 255, 255

#range of green color
lg = np.array(lowerLimitGreen) 
ug = np.array(upperLimitGreen)
#range of red color
lr = np.array(lowerLimitRed) 
ur = np.array(upperLimitRed)

count = 0

def classifyGR(img):
    global count
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert the image into hsv
    
    green_mask = cv2.inRange(hsv, lg, ug) #green masked image
    cv2.imshow('green', green_mask) #show the image 
    
    red_mask = cv2.inRange(hsv, lr, ur) #red masked image
    cv2.imshow('red', red_mask)  #show the image
    
    green_counter = 0
    red_counter = 0
    
    for i in range(len(green_mask)):
        for j in range(len(green_mask[i])):
            if(green_mask[i][j] == 0):
                green_counter = green_counter + 1
    
    for i in range(len(red_mask)):
        for j in range(len(red_mask[i])):
            if(red_mask[i][j] == 0):
                red_counter = red_counter + 1
    
    if(green_counter > red_counter):
        my_command = 'forward 20'
        socket.sendto(my_command.encode('utf-8'), tello_address)
    print(green_counter)
    print(red_counter)
    
    count = 0
    return 

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
    my_command = 'takeoff'
    socket.sendto(my_command.encode('utf-8'), tello_address)
    count = count + 1
    ret, frame = capture.read()
    if(ret):
        cv2.imshow('frame', frame)
    if(count == 30):
        classifyGR(frame)
    if cv2.waitKey (1)&0xFF == ord ('q'):
        break
capture.release ()
cv2.destroyAllWindows ()
socket.sendto ('streamoff'.encode (' utf-8 '), tello_address)
