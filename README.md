# IoTcraft for LEGO MINDSTORMS EV3

Simple and lightweight examples of how to connect the LEGO MINDSTORMS EV3 brick to an MQTT server.

## Requirements

- LEGO MINDSTORMS EV3 brick
- MicroSD card (size at least 2GB, **can't be larger than 32GB**)
- USB Wi-Fi dongle (most modern dongles should work)
- [Visual Studio Code](https://code.visualstudio.com/) with the [LEGO® MINDSTORMS® EV3 MicroPython](vscode:extension/lego-education.ev3-micropython) extension
- [Optional] Custom MQTT broker (a public one can be used, such as [test.mosquitto.org](http://test.mosquitto.org/))

## Setup

1. Add the EV3DEV image to your EV3 brick using a microSD card as described in [Getting Started with ev3dev](https://www.ev3dev.org/docs/getting-started/).
2. Connect your EV3 brick to the internet using a USB Wi-Fi dongle. This can be done in the settings of the EV3 brick.
3. Connect your EV3 brick to your computer using a USB cable.
4. Open VS Code and clone this repository to your computer.
5. Pick an example and copy its `main.py` file to the root folder of this repository. (that means at the same level as this `README.md` file)
6. Run the code with the `Download and Run` configuration in the `Run and Debug` tab of VS Code. (Shortcut: `Ctrl + Shift + D`)

## Resources

Here are some additional resources that might be useful:

- <https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3/>
- <https://www.ev3dev.org/docs/getting-started/>
- <https://pybricks.com/ev3-micropython/>
