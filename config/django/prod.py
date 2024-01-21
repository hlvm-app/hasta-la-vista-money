from config.django.base import *  # NOQA

ADMINS = [('Alexander Pavlov', 'alexander.pavlov@pavlovteam.ru')]

CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
SECURE_HSTS_SECONDS = 1800
SECURE_HSTS_PRELOAD = True

# Rosetta
ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_UWSGI_AUTO_RELOAD = False
