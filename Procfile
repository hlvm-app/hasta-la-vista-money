release: python manage.py migrate
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery worker --beat --app hasta_la_vista_money --loglevel info
