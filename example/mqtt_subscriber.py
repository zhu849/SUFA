import paho.mqtt.client as mqtt

# broker setting
# if ip set 127.0.0.1 then mosquitto should opened on terminal
BROKER_IP = "127.0.0.1"
CONNETION_PORT = 1883
CONNETION_TIME = 180
TOPIC_NAME = "tf_status"

def subscribe_listen(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC_NAME)

def recv_msg(client, userdata, msg):
    print(msg.topic+" "+ msg.payload.decode('utf-8'))

client = mqtt.Client()

# set subscribe function
client.on_connect = subscribe_listen
# set account and password
client.username_pw_set("try","xxxx")
# set listen function
client.on_message = recv_msg
# setting connection info (IP, port, connection time)
client.connect(BROKER_IP, 1883, 180)
client.loop_forever()