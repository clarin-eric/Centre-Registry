from os.path import abspath
from os.path import dirname
from os.path import join

from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from centre_registry_project import __name__ as app_name

try:
    VERSION = get_distribution("centre-registry-app").version
except DistributionNotFound:
    VERSION = 'SNAPSHOT'

SECRET_KEY = 'testkey1283182183721'
## Secure cookies have to be turned off in development mode, assuming there is
## no reverse proxy with X-Forwarded-Proto=https or https://tools.ietf.org/html/rfc7239.
DEBUG = True # TODO: templatize
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
PIWIK_WEBSITE_ID = "1000"
PROJECT_DIR = abspath(dirname(__file__))
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django']
TEMPLATE_DEBUG = DEBUG
ADMINS = ('CLARIN ERIC sysops', 'sysops@clarin.eu')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMIN_TITLE = "Centre Registry administration"
MANAGERS = ADMINS
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "HOST": "localhost",
        "USER": "cr",
        "PASSWORD": "",
        "NAME": "cr",
        "PORT": "5432",
    }
}
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
MEDIA_ROOT = ''
STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_DIR,
                   '../../centre-registry-app/centre_registry/assets')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CENTRE_REGISTRY_XSD_URL = 'https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.1/profiles/clarin.eu:cr1:p_1583768728295/xsd'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'centre_registry.context_processors.tracked_by_piwik',
                'centre_registry.context_processors.version',
                'centre_registry.context_processors.centre_profile_xsd_url',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader', )
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.request',
#     'django.contrib.auth.context_processors.auth',
#     'centre_registry.context_processors.tracked_by_piwik',
#     'centre_registry.context_processors.version', )

MIDDLEWARE = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',  # TODO: remove?
    'django.contrib.messages.middleware.MessageMiddleware', )
# TODO: Remove ModelBackend authentication once SSO with RemoteUserBackend is
# in place.
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
ROOT_URLCONF = app_name + '.urls'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  # 'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.admin',
                  'django.contrib.admindocs',
                  'django.contrib.postgres',
                  'django_extensions',
                  'centre_registry',
                  )
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d '
            '%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
            'level': 'DEBUG',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

if DEBUG:
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
