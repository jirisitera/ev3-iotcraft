# IoTcraft for LEGO MINDSTORMS EV3

Simple and lightweight examples of how to connect the LEGO MINDSTORMS EV3 brick to an MQTT server. Written in MicroPython for EV3 by Pybricks.

## Requirements

- LEGO MINDSTORMS EV3 brick
- MicroSD card (size at least 2GB, **can't be larger than 32GB**)
- USB Wi-Fi dongle (most modern dongles will work)
- [Visual Studio Code](https://code.visualstudio.com/) with the [LEGO® MINDSTORMS® EV3 MicroPython](vscode:extension/lego-education.ev3-micropython) extension
- [Optional] Custom MQTT broker (a public one can be used, such as [test.mosquitto.org](http://test.mosquitto.org/))

## Setup

1. Add the EV3DEV image to your EV3 brick using a microSD card as described in [Getting Started with ev3dev](https://www.ev3dev.org/docs/getting-started/).
2. Connect your EV3 brick to the internet using a USB Wi-Fi dongle. This can be done in the settings of the EV3 brick.
3. Connect your EV3 brick to your computer using a USB cable.
4. Open VS Code and clone this repository to your computer.
5. Use the EV3DEV Device Browser to connect to your EV3 brick. This option is in the bottom left corner of VS Code by default.
6. Run the code with the `Download and Run` configuration in the `Run and Debug` tab of VS Code. (Shortcut: `Ctrl + Shift + D`)
7. Start sending messages to the MQTT server on the correct topics. For example, to make a motor on port A run at 10 degrees per second, send the message `10` to the topic `ev3/1234/A`, where 'ev3' and '1234' are unique identifiers defined in the program.

## Resources

Here are some additional resources that might be useful:

- <https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3/>
- <https://www.ev3dev.org/docs/getting-started/>
- <https://pybricks.com/ev3-micropython/>
