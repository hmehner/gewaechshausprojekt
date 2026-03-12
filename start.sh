export $(xargs <.env)

if [ ! -f ./.env ]; then
    cp .env.template .env
fi

python3 version_5.py