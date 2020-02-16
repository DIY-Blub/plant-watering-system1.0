#!/usr/bin/python3
#coding: utf8
#boot.py
import RPi.GPIO as GPIO
import sys
import time
from time import localtime, strftime

# PINS FESTLEGEN
signal_led = 3
strom_sensoren = 5
relais1 = 11
relais2 = 13
relais3 = 15
relais4 = 16
#relais5 = x

# GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(signal_led, GPIO.OUT)
GPIO.setup(strom_sensoren, GPIO.OUT)
GPIO.setup(relais1, GPIO.OUT)
GPIO.setup(relais2, GPIO.OUT)
GPIO.setup(relais3, GPIO.OUT)
GPIO.setup(relais4, GPIO.OUT)
#GPIO.setup(relais5, GPIO.OUT)

# GPIO DEAKTIVIEREN
GPIO.output(strom_sensoren, GPIO.LOW)
GPIO.output(relais1, True)
GPIO.output(relais2, True)
GPIO.output(relais3, True)
GPIO.output(relais4, True)

#ZEIT PRÜFEN UND LED SCHALTEN
zeitpunkt = strftime("%Y", time.localtime())
if zeitpunkt == "1970":
   GPIO.output(signal_led, True)                        # LED AN
else:
   GPIO.output(signal_led, False)                       # LED AUS
