import time
import board
import os
import dht11
import busio
import datetime
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
from dateutil import tz
from suntime import Sun, SunTimeException

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

low = os.getenv('LIGHT_LOW', 35000)
high = os.getenv('LIGHT_HIGH', 60000)
latitude = float(os.getenv('LATITUDE', 51.0504))
longitude = float(os.getenv('longitude', 13.7373))
csv_file = os.getenv('CSV_LOG_FILE', 'sensor_log.csv')

# GPIO Initialisierung
GPIO.setmode(GPIO.BCM)
relay_pin = 21
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)
time.sleep(2)
GPIO.output(relay_pin, GPIO.HIGH) 

# Sonne-Zeiten Initialisierung
sun = Sun(latitude, longitude)
today = datetime.datetime.now()
timezone = datetime.datetime.now().astimezone().tzname()

today_sr = sun.get_sunrise_time(today, tz.gettz(timezone))
today_ss = sun.get_sunset_time(today, tz.gettz(timezone))

print('Today the sun raised at {} and get down at {} {}'.
      format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M'), timezone))

try:
    low = float(low)
    high = float(high)
    latitude = float(latitude)
    longitude = float(longitude)
except:
    print("Umgebungsvariable nicht erkannt, oder konnten nicht zu float umwandeln!")



# Endlosschleife zur kontinuierlichen Messung und Anzeige
def main ():
    try:
        temperature_c, humidity = readTempAndHumidity(dht11_sensor)

        lux = readLight(
            bh1750_bus, 
            DEVICE, 
            ONE_TIME_HIGH_RES_MODE_1
        )

        status = evaluate_light(
            lux, 
            low, 
            high
        )

        logValuesToCSV(
            temperature_c, 
            humidity, 
            lux, 
            csv_file
        )
        
        renderMatrix(
            status, 
            lux, 
            matrix_device
        )
        
        updateLighting(
            status,
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
       
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(2)
        GPIO.output(relay_pin, GPIO.HIGH) 

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

if __name__ == "__main__":
    while True:
        main()
