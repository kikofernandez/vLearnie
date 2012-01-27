# Django settings for msf project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'msf3',
        #'ENGINE': 'sqlite3',
        #'NAME': 'msflite',# 'msf3'#'msf5',#'msf',#'os.path.join(SITE_ROOT, msf.db)' ,                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'moodle': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'moodle1910',#'msf2',#'msf',#'os.path.join(SITE_ROOT, msf.db)' ,                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306', # mandatory
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin_media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
ADMIN_MEDIA_URL = '/media/admin/'

#ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, '/media/admin/')

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'b^jpb*uf^!r!sctu2zr-ry26r=wx7i77o#!o!t$&l*o3)r)$#0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "msf.context_processors.admin_media",
    "django.contrib.messages.context_processors.messages",
    )

#OUTPUT_VALIDATOR_VALIDATORS = {
#  #'text/html': '/usr/bin/validate',
#  #'application/xml+xhtml': '/usr/bin/validate',
#}

# First will always look for the 'django_language' cookie, if not,
# look for this cookie (in Moodle is is 'lang')
#LANGUAGE_COOKIE_NAME = 'lang'

LANGUAGE_CODE = 'es-es'
ugettext = lambda s: s

LANGUAGES = (
  ('es', ugettext('Spanish')),
  ('en', ugettext('English')),
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'output_validator.middleware.ValidatorMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # for recognizing different languages
    'django.middleware.locale.LocaleMiddleware',
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

#INTERNAL_IPS = ('127.0.0.1',)

AUTHENTICATION_BACKENDS = (
    #'api.authentication.backend.MSFAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    'authentication.backend.MD5Authentication',
    'session.backend.MoodleSessionBackend',
)

SESSION_ENGINE = 'session.handshake'#'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/Applications/xampp/moodledata/sessions/'
#SESSION_FILE_PATH = '/tmp'
# Debe de corresponder a sessionid pues es el nombre por el que es reconocida la session
# Corresponde al nombre del fichero, es decir, sess_XXXXX donde XXXX es el valor conocido como
# sessionid.

#SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_NAME = 'MoodleSession'
#SESSION_COOKIE_NAME = 'sessionid' # 'session_id'

ROOT_URLCONF = 'msf.urls'

LOGIN_URL = 'http://localhost/moodle1910/'

#MOODLE_SITE_DOMAIN = 'localhost/moodle1910'
MINUTES_ACTIVE_SESSION = 3000000

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

# CACHE OPTIONS FOR USING MEMCACHED
#CACHE_BACKEND = 'locmem://'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=3000&max_entries=400'
#CACHE_BACKEND = 'memcached://msf.com:11211/?timeout=3000&max_entries=1000'
#CACHE_BACKEND = 'redis_cache.cache://127.0.0.1:6379/'
#CACHE_BACKEND = 'dummy://'
#CACHE_MIDDLEWARE_SECONDS = 30
#CACHE_MIDDLEWARE_KEY_PREFIX = ''


#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
#)

FHY_MAX_FILE_SIZE = 1024*1024

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # No usado debido a que vamos a usar sessiones en ficheros
    #'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'tagging',
    'coltrane',
#    'debug_toolbar',
    'portfolio',
    'space',
    'community',
    'fhy',
    'friendycontrol',
    'piston',
    'socialmedia_reference',
    #'output_validator',
    #'django-piston',
)
