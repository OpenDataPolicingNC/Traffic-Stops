from traffic_stops.settings.staging import *  # noqa

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'traffic_stops_production'

PUBLIC_ROOT = '/var/www/traffic-stops-production/public/'

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

EMAIL_SUBJECT_PREFIX = '[Traffic Stops Prod] '

DEFAULT_FROM_EMAIL = 'noreply@foobar.com'

# Uncomment if using celery worker configuration
BROKER_URL = 'amqp://traffic_stops:%s@127.0.0.1:5672/traffic_stops_production' % os.environ['BROKER_PASSWORD']
