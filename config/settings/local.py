from base import *

LOCAL_SETTINGS_LOADED = True

DEBUG = True

INTERNAL_IPS = ('127.0.0.1', )

ADMINS = (
    ('Your Name', 'username@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'example_site',  # Or path to database file if using sqlite3.
        'USER': 'example_site',                                        # Not used with sqlite3.
        'PASSWORD': '<enter a new secure password>',
        'HOST': 'localhost',
    }
}
