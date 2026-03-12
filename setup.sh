#!/bin/bash

echo "#####"
echo "Setting up InfluxDB..."


sudo apt update
sudo apt install -y influxdb

sudo systemctl enable influxdb
sudo systemctl start influxdb

echo "Done setting up InfluxDB..."
echo "#####"



echo "#####"
echo "Setting up Grafana..."

sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt-get update
sudo apt-get install -y grafana

sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server

echo "Done setting up Grafana..."
echo "#####"