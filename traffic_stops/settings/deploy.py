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
DATABASES['traffic_stops_il']['NAME'] = 'traffic_stops_il_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_il']['USER'] = 'traffic_stops_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_il']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['traffic_stops_il']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['traffic_stops_il']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')
DATABASES['traffic_stops_md']['NAME'] = 'traffic_stops_md_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_md']['USER'] = 'traffic_stops_%s' % ENVIRONMENT.lower()
DATABASES['traffic_stops_md']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['traffic_stops_md']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['traffic_stops_md']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')
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
        # Check tsdata.utils.flush_memcached when changing this.
        'BACKEND': 'caching.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

ADMINS = (
    ('ODP Team', 'odp-team@caktusgroup.com'),
)
MANAGERS = ADMINS

SERVER_EMAIL = 'no-reply@opendatapolicingnc.com'
DEFAULT_FROM_EMAIL = 'no-reply@opendatapolicingnc.com'

EMAIL_SUBJECT_PREFIX = '[Traffic_Stops %s] ' % ENVIRONMENT.title()

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = [os.environ['DOMAIN']]

# Uncomment if using celery worker configuration
CELERY_SEND_TASK_ERROR_EMAILS = True
BROKER_URL = 'amqp://traffic_stops_%(ENVIRONMENT)s:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/traffic_stops_%(ENVIRONMENT)s' % os.environ  # noqa

LOGGING['handlers']['file']['filename'] = '/var/www/traffic_stops/log/traffic_stops.log'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': []
}

NC_AUTO_IMPORT_DIRECTORY = '/var/www/traffic_stops/NC-automated-import'

# Environment overrides
# These should be kept to an absolute minimum
if ENVIRONMENT.upper() == 'LOCAL':
    # Don't send emails from the Vagrant boxes
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if ENVIRONMENT.upper() == 'PRODUCTION':
    CELERYBEAT_SCHEDULE['automatic-nc-import']['schedule'] = \
        crontab(day_of_month='1', hour=3, minute=0)

    # List of email addresses that receive the report of non-compliance of
    # traffic stop reporting.
    COMPLIANCE_REPORT_LIST = ('Ianmance@southerncoalition.org',)
