#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from umqtt.robust import MQTTClient
import urandom
import time
import config

CLIENT_ID = 'ev3_' + ''.join(urandom.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for _ in range(6))
MAIN_TOPIC = 'ev3/robot'

leftMotor = Motor(Port.A)
rightMotor = Motor(Port.D)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=55.5, axle_track=104)

client = MQTTClient(CLIENT_ID, config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD)
client.connect()

def callback(topic, msg):
  message = msg.decode()
  if topic == MAIN_TOPIC.encode():
    if message == 'stop':
      robot.stop()
    elif message.lstrip('-').isdigit():
      brick.display.text(str(message))
      robot.drive(-int(message), 0)

client.set_callback(callback)
client.subscribe(MAIN_TOPIC)

while True:
  client.check_msg()
  time.sleep(0.1)
