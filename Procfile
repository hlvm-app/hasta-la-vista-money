web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery --app=hasta_la_vista_money worker -l INFO
