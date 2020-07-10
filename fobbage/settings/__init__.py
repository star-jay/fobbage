"""
Django settings for fobbage project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a74ph#-fs7&ql!(af2s4@e5cx@rp0qfj0lgi*^x0+zvg38b$-z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'fobbage.herokuapp.com',
    'localhost',
    '127.0.0.1',
    '192.168.0.141',
    '0.0.0.0',
]
PORTS = ['8080', '8000', '80']

MY_HOSTS = env.list('HOSTNAMES', default=[])
for host in MY_HOSTS:
    ALLOWED_HOSTS.append(host)

ALLOWED_HOSTS_AND_PORTS = [
    f"{hostname}:{port}"
    for port in PORTS
    for hostname in ALLOWED_HOSTS
]

CORS_ORIGIN_WHITELIST = [
    'http://'+host
    for host in ALLOWED_HOSTS_AND_PORTS
]
CORS_ORIGIN_WHITELIST += [
    'https://'+host
    for host in ALLOWED_HOSTS_AND_PORTS
]

# Application definition

INSTALLED_APPS = [
    # Disable runserver's static file serving
    'whitenoise.runserver_nostatic',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'bulma',
    'channels',

    # fobbage
    'fobbage',
    'fobbage.quizes',
    'fobbage.accounts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'spa.middleware.SPAMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CSRF_USE_SESSIONS = False

ROOT_URLCONF = 'fobbage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

LOGOUT_REDIRECT_URL = 'index'

WSGI_APPLICATION = 'fobbage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='postgres:///fobbage'),
}

AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dist'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # noqa

# Single page application https://github.com/metakermit/django-spa
STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'django.contrib.auth.backends.ModelBackend',
    ),
}

ASGI_APPLICATION = 'fobbage.routing.application'

# if you have a redis url(heroku) connect to that, else use a local redis
# $ sudo docker run -p 6379:6379 -d redis:2.8
REDIS_URL = os.environ.get("REDIS_URL", ('localhost', 6379))

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL, ],
        },
    },
}


# CSRF
# CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

# contrib auth
# LOGIN_REDIRECT_URL = 'index'
# for contrib .sites
# SITE_ID = 1
