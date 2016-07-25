from os.path import abspath
from os.path import dirname
from os.path import join

from centre_registry_project import __name__ as app_name
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

try:
    VERSION = get_distribution("centre-registry-app").version
except DistributionNotFound:
    VERSION = 'SNAPSHOT'

# Resource location URLS relative to STATIC_URL.
RESOURCE_LOCATION_DATATABLES = 'libs/DataTables-1.10.6/'
RESOURCE_LOCATION_CLARIN_STYLE = 'CLARIN_style/1.0/'

SECRET_KEY = 'testkey1283182183721'
# Secure cookies have to be turned off in development mode, as the website is
# served over HTTP instead of HTTPS.
# TODO: address
DEBUG = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
PIWIK_WEBSITE_ID = None
PROJECT_DIR = abspath(dirname(__file__))
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
TEMPLATE_DEBUG = DEBUG
ADMINS = ('CLARIN ERIC sysops', 'sysops@clarin.eu')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
GRAPPELLI_ADMIN_TITLE = "Centre Registry administration"
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
}
TIME_ZONE = None  # 'Europe/Berlin'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
MEDIA_ROOT = ''  # os.path.join(PROJECT_DIR, "media/")
# MEDIA_URL = 'http://127.0.0.1:8000/static/media/'
# STATIC_URL = '/static/'
STATIC_URL = 'https://infra.clarin.eu/content/Centre_Registry/'
# ADMIN_MEDIA_PREFIX = "http://127.0.0.1:8000/static/admin/"
STATIC_ROOT = join(PROJECT_DIR,
                   '../../centre-registry-app/centre_registry/static')
# TODO: make robust
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_DIR, "media/"),
#     #os.path.join(PROJECT_DIR, "static/"),
# )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader', )
# 'django.template.loaders.filesystem.Loader',
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'centre_registry.context_processors.res_locs_relv_to_static',
    'centre_registry.context_processors.tracked_by_piwik',
    'centre_registry.context_processors.version', )
MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',  # TODO: remove?
    'django.contrib.messages.middleware.MessageMiddleware', )
# TODO: Remove ModelBackend authentication once SSO with RemoteUserBackend is
#  in place.
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
# 'centre_registry.backends.CRRemoteUserBackend',
# 'django.contrib.auth.backends.RemoteUserBackend',
ROOT_URLCONF = app_name + '.urls'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
# TEMPLATE_DIRS = (glob.glob(os.path.join(PROJECT_DIR, "templates/") + "*/"))

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  # 'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'grappelli',
                  'django.contrib.admin',
                  'django.contrib.admindocs',
                  'centre_registry', )
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
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    # INTERNAL_IPS = ('127.0.0.1', '10.0.0.1')
    # DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,}
    # DEBUG_TOOLBAR_PANELS = (
    #     'debug_toolbar.panels.version.VersionDebugPanel',
    #     'debug_toolbar.panels.timer.TimerDebugPanel',
    #     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    #     'debug_toolbar.panels.headers.HeaderDebugPanel',
    #     #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    #     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    #     'debug_toolbar.panels.sql.SQLDebugPanel',
    #     'debug_toolbar.panels.template.TemplateDebugPanel',
    #     'debug_toolbar.panels.cache.CacheDebugPanel',
    #     'debug_toolbar.panels.signals.SignalDebugPanel',
    #     'debug_toolbar.panels.logger.LoggingPanel',
    # )
