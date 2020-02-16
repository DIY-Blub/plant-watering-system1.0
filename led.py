#!/usr/bin/python3
#coding: utf8
#led.py
import RPi.GPIO as GPIO
import sys
import time
from time import localtime, strftime

zeitpunkt = strftime("%Y", time.localtime())
signal_led = 3                                          # PIN Signal-LED

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(signal_led, GPIO.OUT)

if zeitpunkt == "1970":
   GPIO.output(signal_led, True)                        # LED AN
# hier weitere "elif" platzieren um LED einzuschalten (z.B: Wasserstand!)
else:
   GPIO.output(signal_led, False)                       # LED AUS
