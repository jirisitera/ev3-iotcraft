#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color, Align
from pybricks.tools import wait, StopWatch, DataLog, print
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from umqtt.simple import MQTTClient

import time
import os
import config

ev3 = EV3Brick()
motor = Motor(Port.B)

ev3.speaker.beep()
brick.display.text('MQTT Client')

MQTT_ClientID = 'EV3'

MQTT_Topic_Status = 'ev3/Status'
MQTT_Topic_Motor = 'ev3/Motor'

def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))

motor.reset_angle(0)

mqttc = MQTTClient(MQTT_ClientID, config.MQTT_BROKER, keepalive=60)
mqttc.connect()

mqttc.publish(MQTT_Topic_Status, MQTT_ClientID + ' Started')
mqttc.set_callback(getmessages)
mqttc.subscribe(MQTT_Topic_Status)
mqttc.subscribe(MQTT_Topic_Motor)
mqttc.publish(MQTT_Topic_Status, MQTT_ClientID + ' Listening')

while True:
    mqttc.check_msg()
    time.sleep(0.1)
