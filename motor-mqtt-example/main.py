#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from umqtt.robust import MQTTClient
import urandom
import time
import config

# generate random client id
CLIENT_ID = 'ev3_' + ''.join(urandom.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for _ in range(6))

# define topics here
MAIN_TOPIC = 'ev3/motor'
motor = Motor(Port.A)

# connect to the mqtt server
client = MQTTClient(CLIENT_ID, config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD)
client.connect()

# use this function to receive messages
def callback(topic, msg):
    if topic == MAIN_TOPIC.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))

motor.reset_angle(0)

# set the above function as the callback for incoming messages
client.set_callback(callback)

# subscribe to topics here
client.subscribe(MAIN_TOPIC)

# main loop to check for incoming messages
while True:
    client.check_msg()
    time.sleep(0.1)
