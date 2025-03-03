# EV3 IoTcraft

A simple example of how to connect the LEGO MINDSTORMS EV3 brick to an MQTT server.

To make this system work, you need create a new file called `config.py` in the folder of every project with the MQTT broker settings:

```python
# change the values below to your MQTT broker (or use the example values)
MQTT_BROKER = 'test.mosquitto.org'
MQTT_PORT = '1883'
MQTT_USERNAME = ''
MQTT_PASSWORD = ''
```

Requires adding the EV3DEV image to the brick using a microSD card as described in the [Getting Started with ev3dev](https://www.ev3dev.org/docs/getting-started/) guide.

We recommend you use the [LEGO® MINDSTORMS® EV3 MicroPython](vscode:extension/lego-education.ev3-micropython) extension for Visual Studio Code.
