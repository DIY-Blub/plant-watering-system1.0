#!/usr/bin/python3
#coding: utf8
#sensorkal.py
import RPi.GPIO as GPIO
import sys
import spidev
from spidev import SpiDev
import time

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()

    def open(self):
        self.spi.open(self.bus, self.device)
        #self.spi.max_speed_hz = 1000000                 # nur bei Raspbian-Version "Buster" erforderlich!

    def read(self, channel = 0):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        if 0<=adc[1]<=3:
           data = ((adc[1]&3)<<8)+adc[2]
           return data
        else:
           return 0

    def close(self):
        self.spi.close()

# PINS FESTLEGEN
strom_sensoren = 5
# GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(strom_sensoren, GPIO.OUT)

# FÜHLER ABFRAGEN
GPIO.output(strom_sensoren, GPIO.HIGH)
time.sleep(3)

adc = MCP3008()
value0 = adc.read( channel = 0 ) # Den auszulesenden Channel kannst du natürlich anpassen
value1 = adc.read( channel = 1 ) # Den auszulesenden Channel kannst du natürlich anpassen
value2 = adc.read( channel = 2 ) # Den auszulesenden Channel kannst du natürlich anpassen
value3 = adc.read( channel = 3 ) # Den auszulesenden Channel kannst du natürlich anpassen
value4 = adc.read( channel = 4 ) # Den auszulesenden Channel kannst du natürlich anpassen


time.sleep(3)
GPIO.output(strom_sensoren, GPIO.LOW)
time.sleep(0.5)

# Maximalwert eintragen (nie mehr als 1023!)
max = 1023
# Ausgabe
print ("Sensor 1: ",value0," / ",(max - value0) / max * 100)
print ("Sensor 2: ",value1," / ",(max - value1) / max * 100)
print ("Sensor 3: ",value2," / ",(max - value2) / max * 100)
print ("Sensor 4: ",value3," / ",(max - value3) / max * 100)
print ("Sensor 5: ",value4," / ",(max - value4) / max * 100)
