release: python manage.py migrate --fake default
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
