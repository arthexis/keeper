import os
import sys
import dj_database_url

from .log_settings import get_logging_config
from .utils import getenv

# Sites Framework configuration
# This will be automatically updated

SITE_ID = getenv('SITE_ID', 1)

HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')

SITE_NAME = 'keeper'

SITE_DOMAIN = f'{HEROKU_APP_NAME}.herokuapp.com' if HEROKU_APP_NAME else 'localhost:8100'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG', True)

LOGGING = get_logging_config(DEBUG)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', '*9w$$hwtmu*o_-6g8-qppf^&&b5esec8(@cjy%ays285=cvsi*')


ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']


# Application definition

LOCAL_APPS = [
    'systems',
    'sheets',
    'orgs',
    'downtime',
]

INSTALLED_APPS = [
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'django_select2',
    'bootstrap3',
    'whitenoise',
    'datetimewidget',
    'model_utils',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'seed_data',
    'core',
] + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'keeper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'keeper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Use sqlite3 for local development
# When on Heroku, switch to postgres using a DATABASE_URL

DATABASE_URL = dj_database_url.config(conn_max_age=500)

if DATABASE_URL:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'ATOMIC_REQUESTS': True
        }
    }
    DATABASES['default'].update(DATABASE_URL)

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
            'OPTIONS': {
                'timeout': 20,
            },
            'ATOMIC_REQUESTS': True
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Authentication backends
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'orgs.auth.backends.AdminBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# http://whitenoise.evans.io/en/stable/django.html

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Django Admin Bootstrapped

DAB_FIELD_RENDERER = \
    'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'


SITE_HEADER = getenv('SITE_HEADER', "Keeper")

# Email address used as the default from_email for send_mail

DEFAULT_FROM_EMAIL = 'keeper@arthexis.com'


# Write to a file instead of sending an email while DEBUG

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


# Django-Select2 Configuration
# http://django-select2.readthedocs.io/en/latest/django_select2.html

SELECT2_JS = 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.full.min.js'

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


# Redirect back to index after login if no next URL parameter

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}


# Email settings, show below also defaults for sendgrid
# https://sendgrid.com/docs/Integrate/Frameworks/django.html

EMAIL_HOST = getenv('EMAIL_HOST', 'smtp.sendgrid.net')

EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')

EMAIL_PORT = getenv('EMAIL_HOST_PORT', 587)

EMAIL_USE_TLS = True


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Seed data configuration
# This sets which Models can be seeded and which Serializer is used

SEED_DATA_SERIALIZERS = {
    'Template': {
        'model': 'systems.models.CharacterTemplate',
    },
    'Organization': {
        'model': 'orgs.models.Organization',
        'exclude': ('memberships', 'events'),
    },
    'Merit': {
        'model': 'systems.models.Merit',
    }
}

# When generating and installing seed data, this dictionary determines
# what model instances are seeded. The order is preserved when generating and installing.
# Each entry will generate exactly one zipfile.

SEED_DATA_PLAN = {
    'Template': (
        'mage-mtaw',
        'vampire-vtr',
        'changeling-ctl',
        'werewolf-wtf',
    ),
    'Merit': (lambda obj: True),
}

# Directory that will store the seed data

SEED_DATA_DIRECTORY = os.path.join(BASE_DIR, 'content')


# Setting up login providers with django-allauth
# https://django-allauth.readthedocs.io/en/latest/providers.html#facebook
# https://stackoverflow.com/questions/4532721/facebook-development-in-localhost

SOCIALACCOUNT_PROVIDERS = {}

FACEBOOK_APP_ID = getenv('FACEBOOK_APP_ID')

FACEBOOK_APP_SECRET = getenv('FACEBOOK_APP_SECRET')

if FACEBOOK_APP_ID and FACEBOOK_APP_SECRET:

    FACEBOOK_LOGIN_ENABLED = True

    SOCIALACCOUNT_PROVIDERS['facebook'] = {
        'METHOD': 'js_sdk',
        'SCOPE': ['email', ],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.5',
    }


# Magic admin login password

ADMIN_LOGIN_USERNAME = getenv('ADMIN_LOGIN_USERNAME', 'admin')

ADMIN_LOGIN_PASSWORD = getenv('ADMIN_LOGIN_PASSWORD')


# TODO Create a process that automatically puts new users in a default organization

DEFAULT_ORGANIZATION = None

