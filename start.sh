export $(xargs <.env)

if [ ! -f ./.env ]; then
    cp .env.template .env
fi

echo "Test if Time Server exists..."

IS_CONFIGURED=$(sudo grep -E "^NTP=${TIMESERVER}" /etc/systemd/timesyncd.conf)

if [[ ! -z "$IS_CONFIGURED" ]]; then
    echo "Timeserver already configured..."
else
    echo "Configuring Time Server..."
    sudo sed -i -E "s/^#*NTP=.*/NTP=${TIMESERVER}/g" /etc/systemd/timesyncd.conf
    sudo systemctl restart systemd-timesyncd
fi

echo "Starting main programm..."

python3 version_5.py