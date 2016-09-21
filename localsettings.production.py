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

DHIS2_URL = 'http://comet-test.baosystems.com/'
DHIS2_API_URL = 'http://comet-test.baosystems.com/api/'
DHIS2_USERNAME = 'admin'
DHIS2_PASSWORD = 'district'

STATIC_ROOT = 'static'

COUNTRY_LEVEL = 3

SITE_ROOT = '/cuma'
STATIC_URL = SITE_ROOT + '/static/'

if not SITE_ROOT.endswith('/'):
    SITE_ROOT += '/'

LOGIN_URL = SITE_ROOT + 'accounts/login/'
API_ROOT = SITE_ROOT + 'api/'

DEBUG = False

# Edit with domain URL for best security
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_NAME = 'sessionidcuma'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
