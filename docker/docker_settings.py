try:
    from settings import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cuma',
        'USER': 'cuma',
        'PASSWORD': 'cuma',
        'HOST': 'db',
        'PORT': 5432,
    }
}
