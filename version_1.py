import time
import board
import adafruit_dht

sensor = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperature_C = sensor.temperature
        humidity = sensor.humidity
        print ("Temparatur: {:.1f} °C Luchtfeuchte: {}%".format(temperature_C, humidity))
    
    except RuntimeError as error:
        print (error.args[0])
        time.sleep (2.0)
        continue

    except Exception as error:
        raise error
    
    time.sleep (3.0)