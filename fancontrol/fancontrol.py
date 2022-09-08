#!/usr/bin/env python3

import subprocess
import time

from gpiozero import OutputDevice

HIGH_THRESHOLD = 80
MEDIUM_THRESHOLD = 65
LOW_THRESHOLD = 50
OFF_THRESHOLD = 35
GPIO_PIN = 3


def get_temp():
    """Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')


if __name__ == '__main__':

    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()

        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > OFF_THRESHOLD:
            fan.on()
            time.sleep(0.015)
            fan.off()
        elif temp > LOW_THRESHOLD:
            fan.on()
            time.sleep(0.030)
            fan.off()
        elif temp > MEDIUM_THRESHOLD:
            fan.on()
            time.sleep(0.075)
            fan.off()
        elif temp > HIGH_THRESHOLD:
            fan.on()
            time.sleep(0.090)
            fan.off()
