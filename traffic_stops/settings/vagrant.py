from traffic_stops.settings.staging import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'traffic_stops_vagrant'

EMAIL_SUBJECT_PREFIX = '[Traffic Stops Vagrant] '
DEFAULT_FROM_EMAIL = 'noreply@foobar.com'

BROKER_URL = 'amqp://traffic_stops:%s@127.0.0.1:5672/traffic_stops_vagrant' % os.environ['BROKER_PASSWORD']
