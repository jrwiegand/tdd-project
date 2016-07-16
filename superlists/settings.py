"""
Django settings for superlists project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='4$f)2z$!56$+&f^9*v0%gdodvi1dn&bslc(4jaeh$yk#&86kc6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

TEMPLATE_DEBUG = env.bool('DJANGO_DEBUG', default=False)

# This setting is changed by the deploy script
DOMAIN = "localhost"

ALLOWED_HOSTS = [DOMAIN]

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'functional_tests',
    'accounts',
    'lists',
)

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'accounts.authentication.PersonaAuthenticationBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'superlists.urls'

WSGI_APPLICATION = 'superlists.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default=''),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default=''),
        'PORT': env('DB_PORT', default=''),
    }
}

# Security
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'superlists', 'static'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'accounts': {
            'handlers': ['console'],
        },
        'lists': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}
