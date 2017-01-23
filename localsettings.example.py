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

# Existing demo instance, change this to your local instance
DHIS2_URL = 'https://play.dhis2.org/demo/'
DHIS2_API_URL = DHIS2_URL + 'api/'
DHIS2_USERNAME = 'admin'
DHIS2_PASSWORD = 'district'

COUNTRY_LEVEL = 3

LDAP_SERVER = ''
BASE_DN = ''
LDAP_USER = ''
LDAP_PASSWORD = ''
