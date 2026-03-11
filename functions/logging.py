import csv
import os
import time

def logValuesToCSV(temperature, humidity, lux, output_file):
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode='a', newline='') as file:
        fieldnames = ['Timestamp', 'Temperature_C', 'Humidity_Percent', 'Light_Lux']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'Temperature_C': temperature,
            'Humidity_Percent': humidity,
            'Light_Lux': lux
        })