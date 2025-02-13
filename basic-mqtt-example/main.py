#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from umqtt.robust import MQTTClient
import urandom
import time
import config

# generate random client id
pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
CLIENT_ID = 'ev3_' + ''.join(urandom.choice(pool) for _ in range(6))

# define topics here
MAIN_TOPIC = 'ev3'

# connect to the mqtt server
client = MQTTClient(CLIENT_ID, config.MQTT_BROKER)
client.connect()

# use this function to receive messages
def callback(topic, msg):
    if topic == MAIN_TOPIC.encode():
        brick.display.text(str(msg.decode()))

# set the above function as the callback for incoming messages
client.set_callback(callback)

# subscribe to topics here
client.subscribe(MAIN_TOPIC)

# publish a message to the main topic
client.publish(MAIN_TOPIC, CLIENT_ID + ' connected!')

# main loop to check for incoming messages
while True:
    client.check_msg()
    time.sleep(0.1)
