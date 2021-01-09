import socket
import cv2
import numpy as np
from threading import Thread
import time
import keyboard

class ThreadedCamera(object):
    
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)
    '''
    def show_frame(self):
        if(cv2.waitKey(1)&0xFF == ord ('q')):
            self.capture.release ()
        cv2.imshow('frame', self.frame)
        classifyGR(self.frame)
        cv2.waitKey(self.FPS_MS)
    '''
    
    def check_frame(self):
        if keyboard.is_pressed('q'):
            self.capture.release ()
        classifyGR(self.frame)
        cv2.waitKey(self.FPS_MS)

# Set range for red color and  
# define mask 
red_lower = np.array([136, 87, 111], np.uint8) 
red_upper = np.array([180, 255, 255], np.uint8) 
  
# Set range for green color and  
# define mask 
green_lower = np.array([25, 52, 72], np.uint8) 
green_upper = np.array([102, 255, 255], np.uint8) 

def classifyGR(img):
    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert the image into hsv
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernal = np.ones((5, 5), "uint8")
    # For red color 
    red_mask = cv2.dilate(red_mask, kernal) 
    res_red = cv2.bitwise_and(img, img,  
                              mask = red_mask) 
      
    # For green color 
    green_mask = cv2.dilate(green_mask, kernal) 
    res_green = cv2.bitwise_and(img, img, 
                                mask = green_mask) 
    
     # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
    
    areaRed, areaGreen = -1, -1
    for pic, contour in enumerate(contours): 
        areaTemp = cv2.contourArea(contour) 
        if(areaTemp > areaRed):
            areaRed = areaTemp
    # Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, contour in enumerate(contours): 
        areaTemp = cv2.contourArea(contour) 
        if(areaTemp > areaGreen): 
            areaGreen = areaTemp
    
    if(areaGreen > areaRed):
        print('Green')
        socket.sendto('forward 20'.encode('utf-8'), tello_address)
    else:
        print('Red')
    
if __name__ == '__main__':
    # tello set up
    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_address = (tello_ip, tello_port)
    mypc_address = ('192.168.10.3', 12345)
    socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind (mypc_address)
    socket.sendto ('command'.encode (' utf-8 '), tello_address)
    socket.sendto ('streamon'.encode (' utf-8 '), tello_address)
    print ("Start streaming: ")
    
    src = 'udp://0.0.0.0:11111?overrun_nonfatal=1&fifo_size=50000000'
    threaded_camera = ThreadedCamera(src)
    
    # tello start operation
    socket.sendto('takeoff'.encode('utf-8'), tello_address)
    
    while True:
        try:
            #threaded_camera.show_frame()
            threaded_camera.check_frame()
        except AttributeError:
            pass
        if keyboard.is_pressed('q'):
            print('land')
            socket.sendto('land'.encode('utf-8'), tello_address)
            cv2.destroyAllWindows()
            socket.sendto ('streamoff'.encode (' utf-8 '), tello_address)
            socket.close()
