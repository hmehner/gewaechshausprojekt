export $(xargs <.env)

if [ ! -f ./.env ]; then
    cp .env.template .env
fi

echo "Installing packages..."

PACKAGES=(
    python3-suntime
    ntp
)
apt-get install -y "${PACKAGES[@]}"

echo "Test if Time Server exists..."

NTP_CONF="/etc/ntp.conf"
NTP_SERVER="10.254.5.115"

# Check if the server is already configured
if grep -qE "^[[:space:]]*server[[:space:]]+$NTP_SERVER([[:space:]]|$)" "$NTP_CONF"; then
    echo "NTP server '$NTP_SERVER' is already configured."
else
    echo "Configuring NTP server '$NTP_SERVER'..."
    echo "server $NTP_SERVER" >> "$NTP_CONF"
    echo "NTP server added to $NTP_CONF"

    # Optionally restart the NTP service
    if systemctl is-enabled ntpd >/dev/null 2>&1 || systemctl is-active ntpd >/dev/null 2>&1; then
        systemctl restart ntpd
    elif systemctl is-enabled ntp >/dev/null 2>&1 || systemctl is-active ntp >/dev/null 2>&1; then
        systemctl restart ntp
    fi
fi

echo "Starting main programm..."

python3 ./version_5.py