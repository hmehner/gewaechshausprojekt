import board
import os
import time
import dht11
import busio
import smbus
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from adafruit_ht16k33 import segments
from pygments import highlight
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas



# Funktion zum Auslesen des DHT11-Temperatur- und Luftfeuchtigkeitssensors
def readTempAndHumidity(sensor):
    temperature = 0
    humidity = 0

    while temperature == 0 and humidity == 0:
        result = sensor.read()
        temperature = result.temperature
        humidity = result.humidity
        time.sleep(0.5)

    temperature_c = "%-3.1fC" % temperature
    humidity_p = "%-3.1f%%" % humidity
    #Ausgabe im Terminal
    print (temperature_c)
    print (humidity_p)
    return temperature_c, humidity_p



# Funktion zum Auslesen des BH1750-Lichtsensors
def readLight(bus, DEVICE, ONE_TIME_HIGH_RES_MODE_1):
    lux = 0
    while lux == 0:
        data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
        # Rohdaten in Lux umrechnen
        lux = (data[1] + (256 * data[0])) / 1.2
        time.sleep(0.5)
    return lux



# Bewertung für blühenden Nutzhanf (Pharma/Tee)
def evaluate_light(lux, low, high):
    if lux < low:
        return 1
    elif lux > high:
        return 2
    else:
        return 0
        
def updateLighting(status, time, sunrise, sundown):
    if lux < low:
        GPIO.output(relay_pin, GPIO.LOW)
    elif lux > high:
        GPIO.output(relay_pin, GPIO.HIGH)


# Funktion zur Anzeige auf der 8x8 LED-Matrix
def renderMatrix(recommendation, lux, device):
    with canvas(device) as draw:
        if recommendation == 0:
            print(f"Licht: {lux:.1f} Lux Perfekt")
            for x in range(2,6):
                for y in range(2,6):
                    draw.point((x, y), fill="white")
        elif recommendation == 1:
            print(f"Licht: {lux:.1f} Lux Zu dunkel")
            start = 3
            end = 4
            for y in range(2,6):
                for x in range(start, end+1):
                    draw.point((x,y), fill="white")
                start-=1
                end+=1
        elif recommendation == 2:
            print(f"Licht: {lux:.1f} Lux Zu hell")
            start = 0
            end = 7
            for y in range(2,6):
                for x in range(start, end+1):
                    draw.point((x,y), fill="white")
                start+=1
                end-=1
