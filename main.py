#!/usr/bin/env pybricks-micropython
from pybricks.ev3brick import display
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, InfraredSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from umqtt.robust import MQTTClient
import config
import os
import time
# SENSOR TYPE DEFINITIONS
class SensorType():
  ULTRASONIC = 'lego-ev3-us'
  GYRO = 'lego-ev3-gyro'
  COLOR = 'lego-ev3-color'
  TOUCH = 'lego-ev3-touch'
  INFRARED = 'lego-ev3-ir'
# PORT NAME TO DEFINITION CONVERSION
def getPortDefinition(p):
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
# MOTOR DISCOVERY SERVICE
def discoverMotors():
  motors = []
  for path in os.listdir(MOTOR_PATH):
    portName = open(MOTOR_PATH + '/' + path + '/address').readline()[-2:-1]
    CLIENT.subscribe(MAIN_TOPIC + portName)
    motors.append((portName, Motor(getPortDefinition(portName))))
    display.text('Tacho-motor (' + portName + ')')
  return motors
# SENSOR DISCOVERY SERVICE
def discoverSensors():
  sensors = []
  for path in os.listdir(SENSOR_PATH):
    sensorType = open(SENSOR_PATH + '/' + path + '/driver_name').readline().rstrip()
    portName = open(SENSOR_PATH + '/' + path + '/address').readline()[-2:-1]
    port = getPortDefinition(portName)
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
    display.text(sensorName + ' sensor (' + portName + ')')
  return sensors
# CALLBACK FUNCTION - MQTT MESSAGE HANDLER
def callback(topic, msg):
  topicName = topic.decode()
  # don't do anything if the topic is not for this robot
  if not topicName.startswith(MAIN_TOPIC): 
    return
  # messages can only contain speed values for motors
  message = msg.decode()
  port = topicName.split('/')[-1]
  for motor in MOTORS:
    if motor[0] == port:
      if message == '0':
        # stop motor is speed is 0
        motor[1].stop()
      elif message.lstrip('-').isdigit():
        # set motor speed if speed is valid value
        motor[1].run(int(message))
# MAIN PROGRAM
MAIN_TOPIC = config.TOPIC_PREFIX + '/' + config.UUID + '/'
MOTOR_PATH = '/sys/class/tacho-motor'
SENSOR_PATH = '/sys/class/lego-sensor'
SENSOR_TIMER = 0
display.text('[IoTcraft]')
display.text('Booting up')
display.text('My UUID is ' + config.UUID)
# connect to mqtt broker and subscribe to topics
CLIENT = MQTTClient('', config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_USERNAME, config.MQTT_PASSWORD)
CLIENT.connect()
CLIENT.set_callback(callback)
display.text('Connected to MQTT')
# discover motors and sensors
display.text('Discovering parts')
MOTORS = discoverMotors()
SENSORS = discoverSensors()
# main loop
display.text('Waiting for changes')
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
        value = ''
        if sensorType == SensorType.COLOR:
          baseValue = sensorObject.color()
          if baseValue == None:
            value = 'Color not certain enough'
          else:
            value = 'Color detected: ' + str(baseValue)[6:]
        elif sensorType == SensorType.GYRO:
          value = 'Gyro angle: ' + str(sensorObject.angle()) + ' degrees'
        elif sensorType == SensorType.INFRARED:
          value = 'IR distance: ' + str(sensorObject.distance()) + '%'
        elif sensorType == SensorType.TOUCH:
          value = 'Button pressed' if sensorObject.pressed() else 'Button not pressed'
        elif sensorType == SensorType.ULTRASONIC:
          value = 'Sonic distance: ' + str(sensorObject.distance()) + ' mm'
        CLIENT.publish(MAIN_TOPIC + sensor[1], value)
      SENSOR_TIMER = 0
  # wait for next loop cycle
  time.sleep(0.1)
