'''Formula Steering Wheel & CBR600RR Control with DRS'''

# Author: Lim Chae Won
# Organization: SKID Formula Student Team
# License: Apache 2.0
# coding: utf-8

import gc
import math

import dht
import onewire
import time
import array

rp2
# Timer
timer = machine.Timer()

# Configure the RPM Indication LEDs(WS2812B)
NUM_LEDS = 16
PIN_NUM = 22 # Data Pin Num.
brightness = 0.2 # Between 0~1, Higher the value, Brighter the LEDs.

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

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
