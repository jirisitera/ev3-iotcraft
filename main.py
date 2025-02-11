#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from umqtt.robust import MQTTClient
import time
import os
import config

# https://testclient-cloud.mqtt.cool/

motor = Motor(Port.A)

MQTT_ClientID = 'ev3test'

MQTT_Topic_Status = 'ev3/status'
MQTT_Topic_Motor = 'ev3/motor'

def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))

motor.reset_angle(0)

client = MQTTClient(MQTT_ClientID, config.MQTT_BROKER)
client.connect()

client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Started')
client.set_callback(getmessages)
client.subscribe(MQTT_Topic_Status)
client.subscribe(MQTT_Topic_Motor)
client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Listening')

while True:
    client.check_msg()
    time.sleep(0.1)
