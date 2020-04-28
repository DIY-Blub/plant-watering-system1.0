#!/usr/bin/python3
#coding: utf8
#waterpi.py
import RPi.GPIO as GPIO
import sys
import spidev
from spidev import SpiDev
import time
from time import localtime, strftime

# CLASS & FUNCTIONS
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
           per = (918 - data) / 918 * 100               # maximalen Wert testen und 2x eintragen, zB 918; Wert kann nie mehr als 1023 sein!
           return per
        else:
           return 0
    def close(self):
        self.spi.close()

def watering(relay,pump):
    GPIO.output(relay, False)
    time.sleep(pump)
    GPIO.output(relay, True)
    time.sleep(1)


# LOG
zeitpunkt = strftime("%Y-%m-%d %H:%M:00", time.localtime())
sys.stdout = open("datenlog.log", "a")


# PINS FESTLEGEN
strom_sensoren = 5
relais1 = 11
relais2 = 13
relais3 = 15
relais4 = 16
#relais5 = x

# BEZEICHNUNGEN FESTLEGEN (bezogen auf die Sensoren-Nummer)
text1 = "Buchsbaum"
text2 = "Paprika"
text3 = "Tomaten"
text4 = "Petersilie [Kräuter]"          # Teil der Gruppe: Kräuter
text5 = "Schnittlauch [Kräuter]"        # Teil der Gruppe: Kräuter
#text6 = "x"

# PROZENTWERTE (Minimum,Maximum) und PUMPENDAUER (in Sekunden) FESTLEGEN - [MIN,MAX,DAUER]
duerr = [5,15,15]
trocken = [15,25,10]
feucht = [25,35,5]


# GPIO SETUP
GPIO.setwarnings(False)                         # Fehlermeldungen deaktivieren
GPIO.setmode(GPIO.BOARD)
GPIO.setup(strom_sensoren, GPIO.OUT)
GPIO.setup(relais1, GPIO.OUT)
GPIO.setup(relais2, GPIO.OUT)
GPIO.setup(relais3, GPIO.OUT)
GPIO.setup(relais4, GPIO.OUT)
#GPIO.setup(relais5, GPIO.OUT)


# SENSOREN ABFRAGEN
GPIO.output(strom_sensoren, GPIO.HIGH)
time.sleep(1)
adc = MCP3008()
sensor1 = adc.read( channel = 0 )
sensor2 = adc.read( channel = 1 )
sensor3 = adc.read( channel = 2 )
sensor4 = adc.read( channel = 3 )
sensor5 = adc.read( channel = 4 )
#sensor6 = adc.read( channel = 5 )
time.sleep(1)
GPIO.output(strom_sensoren, GPIO.LOW)
time.sleep(0.5)


# PUMPE 1 (Buchsbaum)
print(zeitpunkt+";"+text1+";{:.1f}%".format(sensor1))

if duerr[0] <= sensor1 <= duerr[1]:
   watering(relais1,duerr[2])
elif trocken[0] <= sensor1 <= trocken[1]:
   watering(relais1,trocken[2])
elif feucht[0] <= sensor1 <= feucht[1]:
   watering(relais1,feucht[2])

# PUMPE 2 (Paprika)
print(zeitpunkt+";"+text2+";{:.1f}%".format(sensor2))

if duerr[0] <= sensor2 <= duerr[1]:
   watering(relais2,duerr[2])
elif trocken[0] <= sensor2 <= trocken[1]:
   watering(relais2,trocken[2])
elif feucht[0] <= sensor2 <= feucht[1]:
   watering(relais2,feucht[2])

# PUMPE 3 (Tomaten)
print(zeitpunkt+";"+text3+";{:.1f}%".format(sensor3))

if duerr[0] <= sensor3 <= duerr[1]:
   watering(relais3,18)                       # manuelle Eingabe
elif trocken[0] <= sensor3 <= trocken[1]:
   watering(relais3,15)                       # manuelle Eingabe
elif feucht[0] <= sensor3 <= feucht[1]:
   watering(relais3,12)                        # manuelle Eingabe

# PUMPE 4 [Kräuter]
print(zeitpunkt+";"+text4+";{:.1f}%".format(sensor4))
print(zeitpunkt+";"+text5+";{:.1f}%".format(sensor5))

if (duerr[0] <= sensor4 <= duerr[1]) or (duerr[0] <= sensor5 <= duerr[1]):
   watering(relais4,duerr[2])
elif (trocken[0] <= sensor4 <= trocken[1]) or (trocken[0] <= sensor5 <= trocken[1]):
   watering(relais4,trocken[2])
elif (feucht[0] <= sensor4 <= feucht[1]) or (feucht[0] <= sensor5 <= feucht[1]):
   watering(relais4,feucht[2])

# PUMPE 5 .....
