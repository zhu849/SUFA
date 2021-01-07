import cv2
import numpy as np
import serial
import paho.mqtt.client as mqtt
import json  
import time

### global variable ###
# broker setting
# if ip set 127.0.0.1 then mosquitto should opened on terminal
BROKER_IP = "127.0.0.1"
CONNETION_PORT = 1883
CONNETION_TIME = 180
TOPIC_NAME = "tf_status"
# arduino setting
ARDUINO_SERIAL = 'COM5'
ARDUINO_PORT = 9600
# color image size setting
WIDTH = 1480
HEIGHT = 1000
# traffic light status now
NOW_STATUS = None

def change_green():
    NOW_STATUS = 'green'
    print('Host Now Status: ' + NOW_STATUS)
    # '1' in binary is 49, this action will sent a b'110001 to ardino
    # ardino will use a type of char to receive this char 
    arduino.write('1'.encode())
    
def change_red():
    NOW_STATUS = 'red'
    print('Host Now Status: ' + NOW_STATUS)
    # '2' in binary is 50, this action will sent a b'110010 to ardino
    # ardino will use a type of char to receive this char 
    arduino.write('2'.encode())
    
# send message notify broker
def send_to_broker(client, msg):
    # set payload
    payload = {'status' : msg}
    client.publish(TOPIC_NAME, json.dumps(payload))
    print ("Send payload to broker: ", json.dumps(payload))
    
if __name__ == '__main__':
    # connection with arduino serial 
    arduino = serial.Serial(ARDUINO_SERIAL, ARDUINO_PORT)
    
    # broker connection
    client = mqtt.Client()
    # set connection information
    client.connect(BROKER_IP, CONNETION_PORT, CONNETION_TIME)
    
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
            send_to_broker(client, "start")
            change_green()
            cv2.imshow('Traffic Light',np_green)
            break;

    # control traffic light
    while(True):
        # read from arduino serial port
        arduino_msg = arduino.readline()
        arduino_msg = arduino_msg.decode("utf-8")
        # others times arduino always return msg = '0'
        # return msg = '8' mean success, '9' mean failure
        # define logic is on arduino hardware
        if(arduino_msg == "8\r\n"):
            send_to_broker(client, 'success!')
        elif(arduino_msg == "9\r\n"):
            send_to_broker(client, 'failure!')
        
        keyin = cv2.waitKey(1) & 0xFF
        # turn light to green
        if (keyin == ord('g')):
            change_green()
            cv2.imshow('Traffic Light',np_green)
        # turn light to red
        elif (keyin == ord('r')):
            change_red()
            cv2.imshow('Traffic Light',np_red)
        # exit the exam
        elif (keyin == ord('q')):
            arduino.close()
            send_to_broker(client, "end")     
            cv2.destroyAllWindows() 
            break;
        