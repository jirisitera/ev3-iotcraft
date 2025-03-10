#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, InfraredSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from umqtt.robust import MQTTClient
import config
import os
import time
import urandom
# define sensor types
class SensorType():
  ULTRASONIC = 'lego-ev3-us'
  GYRO = 'lego-ev3-gyro'
  COLOR = 'lego-ev3-color'
  TOUCH = 'lego-ev3-touch'
  INFRARED = 'lego-ev3-ir'
# converts port names to port definitions
def toPort(p):
  if p == 'A':
    return Port.A
  elif p == 'B':
    return Port.B
  elif p == 'C':
    return Port.C
  elif p == 'D':
    return Port.D
  elif p == '1':
    return Port.S1
  elif p == '2':
    return Port.S2
  elif p == '3':
    return Port.S3
  elif p == '4':
    return Port.S4
# discovery service for motors
def createMotorList():
  motors = []
  dirs = os.listdir(MOTOR_DIR)
  for dir in dirs:
    f = open(MOTOR_DIR + '/' + dir + '/' + PORT_FILE)
    portName = f.readline()[-2:-1]
    port = toPort(portName)
    CLIENT.subscribe(MAIN_TOPIC + '/' + portName)
    motors.append((portName, Motor(port)))
    ev3brick.display.text("Motor (port " + portName + ")")
  return motors
# discovery service for sensors
def createSensorList():
  sensors = []
  dirs = os.listdir(SENSOR_DIR)
  for dir in dirs:
    f = open(SENSOR_DIR + '/' + dir + '/' + TYPE_FILE)
    sType = f.readline().rstrip()
    f = open(SENSOR_DIR + '/' + dir + '/' + PORT_FILE)
    portName = f.readline()[-2:-1]
    port = toPort(portName)
    if sType == SensorType.COLOR:
      sensors.append((SensorType.COLOR, portName, ColorSensor(port)))
      ev3brick.display.text("Color sensor (port " + portName + ")")
    elif sType == SensorType.GYRO:
      sensors.append((SensorType.GYRO, portName, GyroSensor(port)))
      ev3brick.display.text("Gyro sensor (port " + portName + ")")
    elif sType == SensorType.INFRARED:
      sensors.append((SensorType.INFRARED, portName, InfraredSensor(port)))
      ev3brick.display.text("Infrared sensor (port " + portName + ")")
    elif sType == SensorType.TOUCH:
      sensors.append((SensorType.TOUCH, portName, TouchSensor(port)))
      ev3brick.display.text("Touch sensor (port " + portName + ")")
    elif sType == SensorType.ULTRASONIC:
      sensors.append((SensorType.ULTRASONIC, portName, UltrasonicSensor(port)))
      ev3brick.display.text("Ultrasonic sensor (port " + portName + ")")
  return sensors
# callback for mqtt messages
def callback(topic, msg):
  topicName = topic.decode()
  if not topicName.startswith(MAIN_TOPIC):
    return
  message = msg.decode()
  port = topicName.split('/')[-1]
  for motor in MOTORS:
    if motor[0] == port:
      if message == '0':
        motor[1].stop()
      elif message.lstrip('-').isdigit():
        motor[1].run(int(message))
# define constants
PREFIX = 'ev3'
CLIENT_ID = PREFIX + '_' + ''.join(urandom.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for _ in range(6))
UUID = '1234'
MAIN_TOPIC = PREFIX + '/' + UUID
MOTOR_DIR = '/sys/class/tacho-motor'
SENSOR_DIR = '/sys/class/lego-sensor'
TYPE_FILE = 'driver_name'
PORT_FILE = 'address'
SENSOR_TIMER = 0
# register mqtt client
CLIENT = MQTTClient(CLIENT_ID, config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD)
CLIENT.connect()
CLIENT.set_callback(callback)
# register motors and sensors
MOTORS = createMotorList()
SENSORS = createSensorList()
# main loop
while True:
  # receive messages
  CLIENT.check_msg()
  # publish messages
  if (SENSORS != []):
    SENSOR_TIMER += 1
    if SENSOR_TIMER >= 50:
      for sensor in SENSORS:
        sensorType = sensor[0]
        sensorPort = sensor[1]
        sensorObject = sensor[2]
        if sensorType == SensorType.COLOR:
          CLIENT.publish(MAIN_TOPIC + '/' + sensorPort, str(sensorObject.color()))
        elif sensorType == SensorType.GYRO:
          CLIENT.publish(MAIN_TOPIC + '/' + sensorPort, str(sensorObject.angle()))
        elif sensorType == SensorType.INFRARED:
          CLIENT.publish(MAIN_TOPIC + '/' + sensorPort, str(sensorObject.distance()))
        elif sensorType == SensorType.TOUCH:
          CLIENT.publish(MAIN_TOPIC + '/' + sensorPort, str(sensorObject.pressed()))
        elif sensorType == SensorType.ULTRASONIC:
          CLIENT.publish(MAIN_TOPIC + '/' + sensorPort, str(sensorObject.distance()))
      SENSOR_TIMER = 0
  # wait for next loop cycle
  time.sleep(0.1)
