from .settings import *

DATABASES['default'].update({
    'HOST': 'localhost',
    'PORT': 5556,
    'USER': 'postgres',
    'PASSWORD': 'secretpass',
})

SETTINGS_FILE = os.path.basename(__file__)

