from traffic_stops.settings.base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'traffic_stops_staging'

PROVISION_ROOT = os.path.dirname(PROJECT_ROOT)
PUBLIC_ROOT = os.path.join(PROVISION_ROOT, 'public')
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')
LOG_ROOT = os.path.join(PROVISION_ROOT, 'log')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_SUBJECT_PREFIX = '[Traffic Stops Staging] '
ADMINS = (
    ('Colin Copeland', 'ccopeland@codeforamerica.org'),
)
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'noreply@foobar.com'

COMPRESS_ENABLED = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = ('*',)

SECRET_KEY = os.environ['SECRET_KEY']

BROKER_URL = 'amqp://traffic_stops:%s@127.0.0.1:5672/traffic_stops_staging' % os.environ['BROKER_PASSWORD']

LOGGING['handlers']['file']['filename'] = os.path.join(LOG_ROOT, 'traffic-stops-django.log')
LOGGING['loggers']['celery'] = {
    # mail_admins will only accept ERROR and higher
    'handlers': ['mail_admins', 'file'],
    'level': 'INFO',
}
# 'django' is the catch-all logger
LOGGING['loggers']['django'] = {
    # mail_admins will only accept ERROR and higher
    'handlers': ['mail_admins', 'file'],
    'level': 'INFO',
}


# A simple task to make sure Celery is running
CELERYBEAT_SCHEDULE = {
    'test-celery-health': {
        'task': 'traffic_stops.celery.debug_task',
        'schedule': 30  # seconds
    }
}
