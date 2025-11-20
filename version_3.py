import time
import board
import dht11
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from adafruit_ht16k33 import segments

# Initialisierung des 7-Segment-Displays und des DHT11-Sensors
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c)
display.fill(0)

# Initialisierung des DHT11-Sensors am Pin D4
sensor = dht11.DHT11(pin = 4)

# Initialisierung des 16x2 LCD Moduls
i2c = busio.I2C(board.SCL, board.SDA)

# Definiere LCD Zeilen und Spaltenanzahl.
lcd_columns = 16
lcd_rows    = 2

lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)
lcd.backlight = True

lcd.clear()
lcd.cursor = True
lcd.message = "Messung wird \ndurchgefuehrt..."

# Endlosschleife zur kontinuierlichen Messung und Anzeige
while True:
    try:
        result = sensor.read()
        temperature_C = "%-3.1fC" % result.temperature
        humidity = "%-3.1f%%" % result.humidity

        # Anzeige der Temperatur 
        display.fill(0)
        display.print (temperature_C)
        #Das ist nur fuer die Ausgabe im Terminal kann man weglassen
        print (temperature_C)
        time.sleep (10)

        # Anzeige der Luftfeuchtigkeit
        display.fill(0)
        display.print (humidity.replace("%", "F"))
        #Das ist nur fuer die Ausgabe im Terminal kann man weglassen
        print (humidity)
        time.sleep (10)

        # Anzeige der Temp. Luftfeuchte auf LCD
        lcd.clear()
        lcd.cursor = True
        lcd.message = f'Temp:    {temperature_C} \nFeuchte: {humidity}'

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
