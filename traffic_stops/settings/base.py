# Django settings for traffic_stops project.
import os

from celery.schedules import crontab

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'traffic_stops',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'traffic_stops_il': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'traffic_stops_il',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'traffic_stops_nc': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'traffic_stops_nc',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'traffic_stops_md': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'traffic_stops_md',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

DATABASE_ROUTERS = ['traffic_stops.routers.StateDatasetRouter']
DATABASE_ETL_USER = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'
IL_TIME_ZONE = 'America/Chicago'
MD_TIME_ZONE = 'America/New_York'
NC_TIME_ZONE = 'America/New_York'

IL_KEY = 'il'
MD_KEY = 'md'
NC_KEY = 'nc'


class StateConfig:
    def __init__(self, tz_name=None):
        self.tz_name = tz_name


STATE_CONFIG = {
    IL_KEY: StateConfig(tz_name=IL_TIME_ZONE),
    MD_KEY: StateConfig(tz_name=MD_TIME_ZONE),
    NC_KEY: StateConfig(tz_name=NC_TIME_ZONE),
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(PROJECT_ROOT, 'node_modules/bootstrap'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY', '0qakm1)=inee683)p)0#lt2o#=@*dy5uw4_nm-1z5gqpy8idbk')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'dealer.contrib.django.context_processor',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'traffic_stops.middleware.StateMiddleware',
)

ROOT_URLCONF = 'traffic_stops.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'traffic_stops.wsgi.application'

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',  # required by django-allauth
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    # External apps
    'selectable',
    'bootstrap3',
    'el_pagination',
    'rest_framework',
    # Custom apps
    'tsdata',
    'nc',
    'md',
    'il',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
SYSLOG_PATH = None
for path in ("/dev/log", "/var/run/syslog"):
    if os.path.exists(path):
        SYSLOG_PATH = path

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
        'papertrail': {
            'format': 'django %(asctime)s %(name)s %(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_ROOT, 'traffic_stops.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_PATH,
            'facility': 'local6',
            'filters': ['require_debug_false'],
            'formatter': 'papertrail',
        },
    },
    'root': {
        'handlers': ['file', 'syslog'],
        'level': 'INFO',
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins', 'syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'traffic_stops': {
            'handlers': ['file', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
        'tsdata': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'nc': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'md': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'caching': {
            'handlers': ['file', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'caching.invalidation': {
            'handlers': ['file', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

CELERYBEAT_SCHEDULE = {
    # Production overrides the schedule
    'automatic-nc-import': {
        'task': 'nc.tasks.download_and_import_nc_dataset',
        'schedule': crontab(day_of_week='monday', hour=3, minute=0),
    },
}

# If using Celery, tell it to obey our logging configuration.
CELERYD_HIJACK_ROOT_LOGGER = False

# https://docs.djangoproject.com/en/1.9/topics/auth/passwords/#password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Make things more secure by default. Run "python manage.py check --deploy"
# for even more suggestions that you might want to add to the settings, depending
# on how the site uses SSL.
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Application settings
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'home'
SELECTABLE_MAX_LIMIT = 30

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60 * 24 * 60  # 60 days
}

CACHE_COUNT_TIMEOUT = 60 * 60 * 24 * 60  # 60 days

CENSUS_API_KEY = ''

NC_AUTO_IMPORT_DIRECTORY = '/tmp/NC-automated-import'

# 0, 1, or 2 e-mail addresses which will be notified after
# automatic NC imports
NC_AUTO_IMPORT_MONITORS = ('odp-team@caktusgroup.com',)
