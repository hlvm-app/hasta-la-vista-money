import os

from dotenv import load_dotenv

load_dotenv()


SESSION_COOKIE_AGE = os.environ.get('SESSION_COOKIE_AGE', default=1209600)
SESSION_COOKIE_HTTPONLY = os.environ.get(
    'SESSION_COOKIE_HTTPONLY', default=True,
)
SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', default='sessionid')
SESSION_COOKIE_SAMESITE = os.environ.get(
    'SESSION_COOKIE_SAMESITE', default='Lax',
)
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', default=False)

CSRF_USE_SESSIONS = os.environ.get('CSRF_USE_SESSIONS', default=True)
