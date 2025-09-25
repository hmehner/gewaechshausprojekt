import time
import board
import dht11
import busio
from adafruit_ht16k33 import segments

# Initialisierung des 7-Segment-Displays und des DHT11-Sensors
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c)
display.fill(0)

# Initialisierung des DHT11-Sensors am Pin D4
sensor = dht11.DHT11(pin = 4)

# Endlosschleife zur kontinuierlichen Messung und Anzeige
while True:
    try:
        result = sensor.read()
        temperature_C = result.temperature
        humidity = result.humidity

        # Anzeige der Temperatur 
        display.fill(0)
        display.print ("%-3.1fC" % temperature_C)
        #Das ist nur fuer die Ausgabe im Terminal kann man weglassen
        print ("%-3.1fC" % temperature_C)
        time.sleep (5.0)

        # Anzeige der Luftfeuchtigkeit
        display.fill(0)
        display.print ("%-3.1f%%" % humidity)
        #Das ist nur fuer die Ausgabe im Terminal kann man weglassen
        print ("%-3.1f%%" % humidity)
        time.sleep (5.0)

    except RuntimeError as error:
        print (error.args[0])
        time.sleep (2.0)
        continue

    except Exception as error:
        raise error
