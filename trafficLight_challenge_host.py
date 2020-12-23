import cv2
import numpy as np
import serial

# color image size
WIDTH = 1280
HEIGHT = 1000
# traffic light status now
NOW_STATUS = None
# connection with arduino dev/port
arduino = serial.Serial('COM5',9600)

def change_green():
    NOW_STATUS = 'green'
    print('Now Status: ' + NOW_STATUS)
    # '1' in binary is 49, this action will sent a b'110001 to ardino
    # ardino will use a type of char to receive this char 
    arduino.write('1'.encode())
    
def change_red():
    NOW_STATUS = 'red'
    print('Now Status: ' + NOW_STATUS)
    # '2' in binary is 50, this action will sent a b'110010 to ardino
    # ardino will use a type of char to receive this char 
    arduino.write('2'.encode())
    
# send 'start' or 'end' message notify broker
def send_to_broker(msg):
    print('Send '+ msg +' msg to broker.')
    # send msg to broker

    
if __name__ == '__main__':
    # construct image array with color black, red, green
    np_black = np.zeros(HEIGHT*WIDTH*3).reshape(HEIGHT,WIDTH,3)
    np_red = np.copy(np_black)
    np_green = np.copy(np_black)

    # construct red & green image
    for i in range(HEIGHT):
        for j in range(WIDTH):
            np_red[i][j][2] = 255
            np_green[i][j][1] = 255

    # initial window show
    cv2.imshow('Traffic Light',np_black)

    # start exam
    # waitting for 's' button hitted to start exam, then initial STATUS is green
    while(True):
        if (cv2.waitKey(1) & 0xFF) == ord('s'):
            send_to_broker("start")
            change_green()
            cv2.imshow('Traffic Light',np_green)
            break;

    # control traffic light
    while(True):
        # turn light to green
        if (cv2.waitKey(1) & 0xFF) == ord('g'):
            change_green()
            cv2.imshow('Traffic Light',np_green)
        # turn light to red
        elif (cv2.waitKey(1) & 0xFF) == ord('r'):
            change_red()
            cv2.imshow('Traffic Light',np_red)
        # exit the exam
        elif (cv2.waitKey(1) & 0xFF) == ord('q'):
            arduino.close()
            send_to_broker("end")     
            cv2.destroyAllWindows() 
            break;