"""
Django settings for CUMA project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kc!kfz)p$es1epeu^@sc4pr%8izl7&xjssvu51iw5vv60&%k%%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'accounts',
    'dhis2',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cuma',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'bower_components')]

DHIS2_API_URL = ''
DHIS2_API_VERSION = '25'
DHIS2_USERNAME = ''
DHIS2_PASSWORD = ''

COUNTRY_LEVEL = 3

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTH_USER_MODEL = 'accounts.DHIS2User'

AUTHENTICATION_BACKENDS = (
    'dhis2.auth.DHIS2Authentication',
)

LANGUAGES = [
    ('ar', 'Arabic'),
    ('ar_EQ', 'Arabic (Egypt)'),
    ('ar_IQ', 'Arabic (Iraq)'),
    ('ar_SD', 'Arabic (Sudan)'),
    ('bn', 'Bengali'),
    ('bi', 'Bislama'),
    ('my', 'Burmese'),
    ('zh', 'Chinese'),
    ('dz', 'Dzongkha'),
    ('en', 'English'),
    ('fr', 'French'),
    ('in_ID', 'Indonesian (Indonesia)'),
    ('km', 'Khmer'),
    ('rw', 'Kinyarwanda'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('mn', 'Mongolian'),
    ('ne', 'Nepali'),
    ('pt', 'Portuguese'),
    ('pt_BR', 'Portuguese (Brazil)'),
    ('ru', 'Russian'),
    ('es', 'Spanish'),
    ('tg', 'Tajik'),
    ('tet', 'Tetum'),
    ('ur', 'Urdu'),
    ('vi', 'Vietnamese'),
]


DEFAULT_ROLES = [
    'Aggregate Data Entry',
    'Analytics',
    'Individual Data Entry'
]

LDAP_SERVER = ''
BASE_DN = ''
LDAP_USER = ''
LDAP_PASSWORD = ''

try:
    from localsettings import *
except ImportError:
    pass
