
from pathlib import Path

import environ
import os
import platform

WINDOWS = platform.system() == "Windows"

if WINDOWS:
    # the below needs to change for linux
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W\bin\gdal304.dll'
    GEOS_LIBRARY_PATH = r'C:\OSGeo4W\bin\geos_c.dll'
    OSGEO4W = r"C:\OSGeo4W"
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = "C:\Program Files\GDAL\gdal-data" + \
        r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", False)

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="wnZ7IbdiGzck7uwX1u5oK2e90iPZy8E5BxHY8H0I1khDKGZHwvxIikLCtkrngJ8X",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'home',
    'members.apps.MembersConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # "django.contrib.sites",
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.forms",

    "crispy_forms",
    # "crispy_bootstrap5",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.gis",
    "rest_framework_gis",
    "corsheaders",
    "drf_spectacular",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (             Specify domains to whitelist
#   'http://localhost:8000',
# )

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["ENGINE"] = 'django.contrib.gis.db.backends.postgis'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },
# }

# DATABASES = {
#     'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': os.environ.get('MYSQL_DBNAME'),
#        'USER': os.environ.get('MYSQL_DBUSER'),
#        'PASSWORD': os.environ.get('MYSQL_DBPASSWORD'),
#        'HOST': os.environ.get('MYSQL_DBHOST'),
#        'PORT': '3306',
#     },

#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('POSTGRES_NAME'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     },
# }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'TakeOver API',
    'DESCRIPTION': 'TakeOver Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


# CONSOLE_LOGGING_FORMAT = '%(asctime)s %(levelname)-8s %(threadName)-14s' \
#     '(%(pathname)s:%(lineno)d) %(name)s.%(funcName)s: %(message)s'
# CONFIG_FILE = os.path.dirname(__file__)
# CONSOLE_LOGGING_FILE_LOCATION = os.path.join(CONFIG_FILE.split(
#     f'config(os.sep)settings')[0], 'django-wrds.log')
# # FORMAT = '%(hostname)s %(asctime)s %(levelname)-8s' \
# #     '%(threadName)-14s (%(pathname)s:%(lineno)d) ' \
# #     '%(name)s.%(funcName)s: %(message)s'
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'loggers': {
#         # Root logger
#         '': {
#             'level': os.getenv('ROOT_LOG_LEVEL', 'INFO'),
#             'handlers': ['file', 'console'],
#         },
#         'django': {
#             # The 'django' logger is configured by Django out of the box. Here, it is reconfigured in order to
#             # utilize the file logger and allow configuration at runtime
#             'handlers': ['file'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#             'propagate': False,
#         },
#         'django.server': {
#             'propagate': True,
#         },
#         'django.http': {
#             'propagate': False,
#             'level': 'DEBUG',
#             'handlers': ['file'],
#         },
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['file'],
#         },
#         'django.security.DisallowedHost': {
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.request': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
#     'formatters': {
#         'my_formatter': {
#             'format': CONSOLE_LOGGING_FORMAT,
#             'style': '%',
#         },
#         "verbose": {
#             "format": "%(levelname)s %(asctime)s %(module)s "
#             "%(process)d %(thread)d %(message)s"
#         },
#     },
#     'handlers': {
#         'console': {
#             "level": "DEBUG",
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': CONSOLE_LOGGING_FILE_LOCATION,
#             'mode': 'a',
#             'encoding': 'utf-8',
#             'formatter': 'my_formatter',
#             'backupCount': 5,
#             'maxBytes': 10485760,
#         },
#     },
# }
