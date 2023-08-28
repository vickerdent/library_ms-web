"""
Django settings for Library_MS project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os, django_heroku, dj_database_url
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!

SECRET_KEY = get_random_secret_key()

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = ["*"]

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 0 # Set to 31536000 (1 year)

SESSION_COOKIE_SECURE = False

CACHE_MIDDLEWARE_ALIAS = "default"

CACHE_MIDDLEWARE_SECONDS = 600

CACHE_MIDDLEWARE_KEY_PREFIX = ""

# Application definition

INSTALLED_APPS = [
    'website',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django_backblaze_b2',
]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = 'Library_MS.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Library_MS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': user,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "django-backblaze-b2": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

BACKBLAZE_CONFIG = {
    # however you want to securely retrieve these values
    "application_key_id": os.getenv("BACKBLAZE_APPLICATION_KEY_ID"),
    "application_key": os.getenv("BACKBLAZE_APPLICATION_KEY"),
    "bucket": os.getenv("BACKBLAZE_BUCKET"),
}

# For Dropbox
# DROPBOX_OAUTH2_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
# DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
# DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
# DROPBOX_OAUTH2_REFRESH_TOKEN = os.getenv("DROPBOX_OAUTH2_REFRESH_TOKEN")
# DROPBOX_ROOT_PATH = "/"
# DROPBOX_TIMEOUT = 100
# DROPBOX_WRITE_MODE = "add"

# For Backblaze (with S3 compatibility)
# AWS_S3_REGION_NAME = "us-east-005"
# AWS_S3_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
