#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from umqtt.robust import MQTTClient
import time
import random
import string
import config

# https://testclient-cloud.mqtt.cool/

ev3 = EV3Brick()

motor = Motor(Port.A)

CLIENT_ID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

TOPIC_STATUS = 'ev3/status'
TOPIC_MOTOR = 'ev3/motor'

def callback(topic, msg):
    if topic == TOPIC_STATUS.encode():
        ev3.screen.print(str(msg.decode()))
    elif topic == TOPIC_MOTOR.encode():
        ev3.screen.print(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))

motor.reset_angle(0)

client = MQTTClient(CLIENT_ID, config.MQTT_BROKER)
client.connect()

client.publish(TOPIC_STATUS, CLIENT_ID + ' started...')
client.set_callback(callback)
client.subscribe(TOPIC_STATUS)
client.subscribe(TOPIC_MOTOR)
client.publish(TOPIC_STATUS, CLIENT_ID + ' listening...')

while True:
    client.check_msg()
    time.sleep(0.2)
