from traffic_stops.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'traffic_stops_production'
DATABASES['default']['USER'] = 'traffic_stops_production'

EMAIL_SUBJECT_PREFIX = '[Traffic Stops Prod] '

# Uncomment if using celery worker configuration
BROKER_URL = 'amqp://traffic_stops_production:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/traffic_stops_production' % os.environ
