from .settings import *
from os import environ

DATABASES['default'].update({
    'HOST': environ.get('POSTGRES_HOST', 'localhost'),
    'PORT': environ.get('POSTGRES_PORT', 5556),
    'USER': environ.get('POSTGRES_USER', 'postgres'),
    'PASSWORD': environ.get('POSTGRES_PASSWORD', 'secretpass'),
})

SETTINGS_FILE = os.path.basename(__file__)

