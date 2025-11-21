import time
import board
import dht11
import busio
import smbus
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from adafruit_ht16k33 import segments
from pygments import highlight

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
lcd.cursor = True
lcd.message = "Messung wird \ndurchgefuehrt..."

# I2C-Bus auswählen und Adresse des BH1750-Sensors
bus = smbus.SMBus(1)
DEVICE = 0x5c
ONE_TIME_HIGH_RES_MODE_1 = 0x20  # einmalige Messung, hohe Auflösung

def readLight():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    # Rohdaten in Lux umrechnen
    return (data[1] + (256 * data[0])) / 1.2

# Bewertung für blühenden Nutzhanf (Pharma/Tee)
def evaluate_light(lux):
    low = 35000
    high = 60000

    if lux < low:
        return "Zu dunkel"
    elif lux > high:
        return "Zu hell"
    else:
        return "Perfekt"

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
                print(f"Licht: {lux:.1f} Lux → {status}")

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