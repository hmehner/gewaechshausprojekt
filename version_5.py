import time
import board
import os
import dht11
import busio
import smbus
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from adafruit_ht16k33 import segments
from pygments import highlight
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Initialisierung des DHT11-Sensors am Pin D4
sensor = dht11.DHT11(pin = 4)

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
bus = smbus.SMBus(1)
DEVICE = 0x5c
ONE_TIME_HIGH_RES_MODE_1 = 0x20  # einmalige Messung, hohe Auflösung

# Initzialisierung der 8x8 LED Matrix
serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90)

low = os.getenv('LIGHT_LOW', 35000)
high = os.getenv('LIGHT_HIGH', 60000)

try:
    low = float(low)
    high = float(high)
except:
    print("Hat Umgebungsvariable für Lichtwerte erkannt, konnte aber nicht zu float umwandeln!")

def readLight():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    # Rohdaten in Lux umrechnen
    return (data[1] + (256 * data[0])) / 1.2

# Bewertung für blühenden Nutzhanf (Pharma/Tee)
def evaluate_light(lux):
    if lux < low:
        return 1
    elif lux > high:
        return 2
    else:
        return 0
    
def renderMatrix(recommendation, lux):
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
                    
            

# Endlosschleife zur kontinuierlichen Messung und Anzeige
def main ():
        while True:
            try:
                result = sensor.read()
                temperature_c = "%-3.1fC" % result.temperature
                humidity = "%-3.1f%%" % result.humidity
                #Ausgabe im Terminal
                print (temperature_c)
                print (humidity)
                lux = readLight()
                status = evaluate_light(lux)
                
                renderMatrix(status, lux)

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
                time.sleep (10)

            except RuntimeError as error:
                print (error.args[0])
                time.sleep (2.0)
                continue

            except KeyboardInterrupt:
                print("Programmende")

                # Anzeigen leeren
                lcd.clear()
                lcd.backlight = False
                display.fill(0)
                exit()

            except Exception as error:
                raise error

if __name__ == "__main__":
    main()
