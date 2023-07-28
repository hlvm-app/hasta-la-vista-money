release: python manage.py migrate
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2