import neopixel
import machine


# Configure the RPM Indication LEDs(WS2812B)
NUM_LEDS = 25
LPIN = machine.Pin.board.x16
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

# 32 LED strip connected to X8.
n = neopixel.NeoPixel(LPIN, NUM_LEDS)

# Draw a red gradient.
for i in range(32):
    n[i] = (i * 8, 0, 0)

# Update the strip.
n.write()
