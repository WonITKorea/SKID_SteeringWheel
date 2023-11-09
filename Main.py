'''Formula Steering Wheel & CBR600RR Control with DRS'''

# Author: Lim Chae Won
# Organization: SKID Formula Student Team
# License: MIT License
# coding: utf-8

import gc
import math
import time
import array
import board
from TempSensor import OBTRead, DHTRead
import time
import machine

# GPIO
machine 

# Timer
timer = machine.Timer()

#Temp Sensor Initialization
OBTemp = OBTRead()
DHTemp = DHTRead()

# Utility functions
def set_in_use(_):
    global in_use

    if in_use:
        in_use = not in_use
        timer.deinit()
        print("Timeout released.")


def in_use_led(in_use):
    if in_use:
        led.set_rgb(64, 0, 0)
    else:
        led.set_rgb(0, 0, 0)


def blink_led(duration, r, g, b):
    led.set_rgb(r, g, b)
    utime.sleep(duration)
    led.set_rgb(0, 0, 0)
