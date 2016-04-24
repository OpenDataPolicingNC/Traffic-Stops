# Settings for live deployed environments: vagrant, staging, production, etc
from .base import *  # noqa

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

ENVIRONMENT = os.environ['ENVIRONMENT']

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

DATABASES['default']['NAME'] = 'traffic_stops_%s' % ENVIRONMENT.lower()
DATABASES['default']['USER'] = 'traffic_stops_%s' % ENVIRONMENT.lower()
DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')
DATABASES['traffic_stops_nc']['NAME'] = 'traffic_stops_nc_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_nc']['USER'] = 'traffic_stops_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_nc']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['traffic_stops_nc']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['traffic_stops_nc']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')
DATABASE_ETL_USER = 'etl'

WEBSERVER_ROOT = '/var/www/traffic_stops/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

LOGGING['handlers']['file']['filename'] = os.path.join(
    WEBSERVER_ROOT, 'log', 'traffic_stops.log')

CACHES = {
    'default': {
        'BACKEND': 'caching.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

ADMINS = (
    ('Colin Copeland', 'ccopeland@codeforamerica.org'),
    ('Andy Shapiro', 'shapiromatron@gmail.com'),
    ('Dylan Young', 'dylanjamesyoung@gmail.com'),
)
MANAGERS = ADMINS

SERVER_EMAIL = 'no-reply@opendatapolicingnc.com'
DEFAULT_FROM_EMAIL = 'no-reply@opendatapolicingnc.com'

EMAIL_SUBJECT_PREFIX = '[Traffic_Stops %s] ' % ENVIRONMENT.title()

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = [os.environ['DOMAIN']]

# Uncomment if using celery worker configuration
CELERY_SEND_TASK_ERROR_EMAILS = True
BROKER_URL = 'amqp://traffic_stops_staging:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/traffic_stops_staging' % os.environ  # noqa

LOGGING['handlers']['file']['filename'] = '/var/www/traffic_stops/log/traffic_stops.log'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': []
}

# Environment overrides
# These should be kept to an absolute minimum
if ENVIRONMENT.upper() == 'LOCAL':
    # Don't send emails from the Vagrant boxes
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
