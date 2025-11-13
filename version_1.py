import time
import board
import busio
from adafruit_ht16k33 import segments
import dht11

# Initialisierung des 7-Segment-Displays und des DHT11-Sensors
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c)
display.fill(0)

# Initialisierung des DHT11-Sensors am Pin D4
sensor = dht11.DHT11(pin = 4)

# Endlosschleife zur kontinuierlichen Messung und Anzeige
while True:
    try:
        temperature_C = sensor.read()

        # Anzeige der Temperatur 
        display.fill(0)
        display.print ("%-3.1fC" % temperature_C.temperature)
        print ("%-3.1fC" % temperature_C.temperature)
        time.sleep (20)

    except RuntimeError as error:
        print (error.args[0])
        time.sleep (2)
        continue

    except Exception as error:
        print(temperature_C)
        raise error
