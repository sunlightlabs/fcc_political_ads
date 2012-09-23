# Django settings for fcc_adtracker project.
from django.template.defaultfilters import slugify
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'project_static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = None

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fcc_adtracker.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fcc_adtracker.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.humanize',

    'sfapp',
    'django_extensions',
    'storages',
    'reversion',
    'mildmoderator',

    'haystack',
    'search',  # Implements the search functionality enabled by haystack

    'doccloud',
    'registration',
    'social_auth',

    'locations',
    'fccpublicfiles',
    'broadcasters',
    'volunteers',

    'south',
    'django_nose',
    'ajax_select',
    
    'scraper',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'organization': ('fccpublicfiles.lookups', 'OrganizationLookup'),
    'advertiser': ('fccpublicfiles.lookups', 'AdvertiserLookup'),
    'media_buyer': ('fccpublicfiles.lookups', 'MediaBuyerLookup'),
    'role_title': ('fccpublicfiles.lookups', 'RoleTitleLookup'),
    'person': ('fccpublicfiles.lookups', 'PersonLookup'),
    'doccloud': ('fccpublicfiles.lookups', 'DocumentCloudLookup'),
    'address': ('fccpublicfiles.lookups', 'AddressLookup'),
    'show_name': ('fccpublicfiles.lookups', 'ShowNameLookup'),
    'broadcaster': ('broadcasters.lookups', 'BroadcasterLookup'),
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

# DocumentCloud
DOCUMENTS_PATH = ''
DOCUMENTCLOUD_USERNAME = ''
DOCUMENTCLOUD_PASS = ''
DOCUMENTCLOUD_DEFAULT_ACCESS_LEVEL = 'public'
DOCUMENTCLOUD_META = {
    'contributedto': 'freethefiles',
    'Collection': 'PoliticalAdSleuth'
}

# Django registration settings
ACCOUNT_ACTIVATION_DAYS = 14
AUTH_PROFILE_MODULE = 'volunteers.Profile'

# Social auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/account/error/'

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/account/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/account/error/'
SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_DEFAULT_USERNAME = lambda u: slugify(u)
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'volunteers.pipeline.account_details',
    'volunteers.pipeline.set_account_details',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'volunteers.pipeline.create_profile',
    'volunteers.pipeline.cleanup',
)

FACEBOOK_EXTENDED_PERMISSIONS = ['email']

#  Search settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '',
        'INDEX_NAME': '',
    },
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


try:
    from local_settings import *
except Exception, e:
    pass
