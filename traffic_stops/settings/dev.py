import sys

from traffic_stops.settings.base import *  # noqa

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

INTERNAL_IPS = ('127.0.0.1', )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOUTH_TESTS_MIGRATE = True

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CACHES = {
    'default': {
        'BACKEND': 'caching.backends.locmem.LocMemCache',
    },
}

NC_AUTO_IMPORT_MONITORS = ()

# Special test settings
if 'test' in sys.argv:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    CACHES['cache_machine'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    NC_AUTO_IMPORT_MONITORS = ('nc-monitor@example.com',)
