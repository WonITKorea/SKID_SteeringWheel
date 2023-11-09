
# Temp Sensor Utilization
from machine import ADC
import adafruit_dht
import time
import board

class OBTRead:
    def __init__(self):
        adcpin = 4
        self.sensor = ADC(adcpin)
def ReadOBT(self):
        adc_value = self.sensor.read_u16()
        volt = (3.3/65535)*adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        return round(temperature, 1)
class DHTRead:
     def __init__(self)
          self.dht = adafruit_dht.DHT22(board.D2)
def ReadDHT(self):
      while True:
        try:
            temperature = self.dht.temperature
            humidity = self.dht.humidity
            # Print what we got to the REPL
            print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
        except RuntimeError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print("Reading from DHT failure: ", e.args)
            time.sleep(1)

# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT