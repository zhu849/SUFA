import paho.mqtt.client as mqtt
BROKER_IP = "140.116.82.164"
CONNETION_PORT = 1883
CONNETION_TIME = 180
TOPIC_NAME = "tf_status"

def sub_broker(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC_NAME)

def encoded_msg(client, userdata, msg):
    print(msg.topic+" "+ msg.payload.decode('utf-8'))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = sub_broker
    client.on_message = on_message
    #client.username_pw_set("try","xxxx")
    client.connect(BROKER_IP, CONNETION_PORT, CONNETION_TIME)
    client.loop_forever()