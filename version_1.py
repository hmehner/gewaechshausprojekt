import time
import board
import adafruit_dht
import busio
from adafruit_ht16k33 import segments

# Initialisierung des 7-Segment-Displays und des DHT11-Sensors
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c)
display.fill(0)

# Initialisierung des DHT11-Sensors am Pin D4
sensor = adafruit_dht.DHT11(board.D4)

# Endlosschleife zur kontinuierlichen Messung und Anzeige
while True:
    try:
        temperature_C = sensor.temperature
        humidity = sensor.humidity

        # Anzeige der Temperatur 
        display.fill(0)
        display.print ("{:2.1f}".format(temperature_C))
        time.sleep (3.0)

    except RuntimeError as error:
        print (error.args[0])
        time.sleep (2.0)
        continue

    except Exception as error:
        raise error
