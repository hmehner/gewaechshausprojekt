import time
import board
import os
import dht11
import busio
import smbus
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
from pygments import highlight
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from functions.sensors import *
from functions.logging import *
from datetime import datetime, date
from suntime import Sun, SunTimeException
from zoneinfo import ZoneInfo
from dateutil import tz


def init():
    # Deklariert relevante Variablen global
    global dht11_sensor
    global i2c
    global display
    global lcd
    global DEVICE
    global ONE_TIME_HIGH_RES_MODE_1
    global high
    global low
    global latitude
    global longitude
    global matrix_device
    global bh1750_bus
    global serial
    global csv_file
    global relay_pin
    global sun

    try:
        low = os.getenv('LIGHT_LOW', 40000)
        high = os.getenv('LIGHT_HIGH', 50000)
        latitude = os.getenv('LATITUDE', 51.0504)
        longitude = os.getenv('LONGITUDE', 13.7373)
        csv_file = os.getenv('CSV_LOG_FILE', 'sensor_log.csv')

        low = float(low)
        high = float(high)
        latitude = float(latitude)
        longitude = float(longitude)
    except Exception as e:
        print(f'Konnte eine Umgebungsvariable nicht richtig einlesen: {e}')

    try:
        # Initialisierung des DHT11-Sensors am Pin D4
        dht11_sensor = dht11.DHT11(pin = 4)

        # Initialisierung des 7-Segment-Displays, des DHT11-Sensors und des LCD Display
        i2c = busio.I2C(board.SCL, board.SDA)
        display = segments.Seg7x4(i2c)
        display.fill(0)

        # Definiere LCD Zeilen und Spaltenanzahl.
        lcd_columns = 16
        lcd_rows    = 2
        lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)
        lcd.backlight = True

        lcd.clear()
        lcd.cursor = False
        lcd.message = "Messung wird \ndurchgefuehrt..."

        # I2C-Bus auswählen und Adresse des BH1750-Sensors
        bh1750_bus = smbus.SMBus(1)
        DEVICE = 0x5c
        ONE_TIME_HIGH_RES_MODE_1 = 0x20  # einmalige Messung, hohe Auflösung

        # Initzialisierung der 8x8 LED Matrix
        serial = spi(port=0, device=1, gpio=noop())
        matrix_device = max7219(serial, cascaded=1, block_orientation=90)

        # GPIO Initialisierung
        GPIO.setmode(GPIO.BCM)
        relay_pin = 21
        GPIO.setup(relay_pin, GPIO.OUT)
        GPIO.output(relay_pin, GPIO.HIGH)
    except Exception as e:
        print(f'Ein Sensor konnte nicht richtig initialisiert werden: {e}')
        exit(1)

    sun = Sun(latitude, longitude)



# Endlosschleife zur kontinuierlichen Messung und Anzeige
def main ():
    try:
        # Hohlt bei jedem Durchlauf neu Datum und Sonnendaten
        current_time = datetime.now()
        today = datetime.now().date()
        today_sr = sun.get_local_sunrise_time(today).replace(tzinfo=None)
        today_ss = sun.get_local_sunset_time(today).replace(tzinfo=None)
        print(f"Sonnenaufgang: {today_sr.strftime('%H:%M')}")
        print(f"Sonnenuntergang: {today_ss.strftime('%H:%M')}")

        # Liest die Temperatur und Luftfeuchte aus
        temperature_c, humidity = readTempAndHumidity(dht11_sensor)

        # Lichtsensor auslesen
        lux = readLight(
            bh1750_bus, 
            DEVICE, 
            ONE_TIME_HIGH_RES_MODE_1
        )

        # Bewertung der Lichtverhältnisse
        status = evaluate_light(
            lux, 
            low, 
            high
        )

        # Beleuchtungsstatus anzeigen
        renderMatrix(
            status, 
            lux, 
            matrix_device
        )

        # Beleuchtungssystem aktualisieren
        lighting = updateLighting(
            status,
            current_time,
            today_sr,
            today_ss
        )
        
        # Logging für CSV
        logValuesToCSV(
            temperature_c, 
            humidity, 
            lux,
            lighting,
            csv_file
        )

        # Anzeige der Temp. und Luftfeuchte auf LCD
        lcd.clear()
        lcd.message = f'Temp:    {temperature_c} \nFeuchte: {humidity}'

        # Anzeige der Temperatur
        display.fill(0)
        display.print (temperature_c)
        time.sleep (10)

        # Anzeige der Luftfeuchtigkeit
        display.fill(0)
        display.print (humidity.replace("%", "F"))
        time.sleep(10) 

    except RuntimeError as error:
        print (error.args[0])

        time.sleep (2.0)
    except KeyboardInterrupt:
        print("Programmende")

        # Anzeigen leeren
        lcd.clear()
        lcd.backlight = False
        display.fill(0)
        GPIO.cleanup()
        exit()
    except Exception as error:
        GPIO.cleanup()
        raise error

# Programmablauf
if __name__ == "__main__":
    init()
    while True:
        main()
