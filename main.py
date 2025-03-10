#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, InfraredSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from umqtt.robust import MQTTClient
import config
import os
import time
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
  for dir in os.listdir(MOTOR_DIR):
    portName = open(MOTOR_DIR + '/' + dir + '/address').readline()[-2:-1]
    CLIENT.subscribe(MAIN_TOPIC + portName)
    motors.append((portName, Motor(toPort(portName))))
    ev3brick.display.text("Tacho-motor (" + portName + ")")
  return motors
# discovery service for sensors
def createSensorList():
  sensors = []
  for dir in os.listdir(SENSOR_DIR):
    sensorType = open(SENSOR_DIR + '/' + dir + '/driver_name').readline().rstrip()
    portName = open(SENSOR_DIR + '/' + dir + '/address').readline()[-2:-1]
    port = toPort(portName)
    if sensorType == SensorType.COLOR:
      sensorName = 'Color'
      sensorObject = ColorSensor(port)
    elif sensorType == SensorType.GYRO:
      sensorName = 'Gyro'
      sensorObject = GyroSensor(port)
    elif sensorType == SensorType.INFRARED:
      sensorName = 'IR'
      sensorObject = InfraredSensor(port)
    elif sensorType == SensorType.TOUCH:
      sensorName = 'Touch'
      sensorObject = TouchSensor(port)
    elif sensorType == SensorType.ULTRASONIC:
      sensorName = 'Ultrasonic'
      sensorObject = UltrasonicSensor(port)
    else:
      continue
    sensors.append((sensorType, portName, sensorObject))
    ev3brick.display.text(sensorName + " sensor (" + portName + ")")
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
MAIN_TOPIC = 'ev3/' + config.UUID + '/'
MOTOR_DIR = '/sys/class/tacho-motor'
SENSOR_DIR = '/sys/class/lego-sensor'
SENSOR_TIMER = 0
ev3brick.display.text("Booting up...")
ev3brick.display.text("My UUID is [" + config.UUID + "]")
# register mqtt client
CLIENT = MQTTClient("", config.MQTT_BROKER, config.MQTT_PORT)
CLIENT.connect()
CLIENT.set_callback(callback)
ev3brick.display.text("Connected to MQTT!")
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
        sensorObject = sensor[2]
        value = ""
        if sensorType == SensorType.COLOR:
          baseValue = sensorObject.color()
          if baseValue == None:
            value = "Color not certain enough"
          else:
            value = "Color detected: " + str(baseValue)[6:]
        elif sensorType == SensorType.GYRO:
          value = "Gyro angle: " + str(sensorObject.angle()) + " degrees"
        elif sensorType == SensorType.INFRARED:
          value = "IR distance: " + str(sensorObject.distance()) + "%"
        elif sensorType == SensorType.TOUCH:
          value = "Button pressed!" if sensorObject.pressed() else "Button not pressed!"
        elif sensorType == SensorType.ULTRASONIC:
          value = "Sonic distance: " + str(sensorObject.distance()) + " mm"
        CLIENT.publish(MAIN_TOPIC + sensor[1], value)
      SENSOR_TIMER = 0
  # wait for next loop cycle
  time.sleep(0.1)
