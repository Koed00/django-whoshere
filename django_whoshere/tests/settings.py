import os

from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "secret_secret_squirrel"
INSTALLED_APPS = global_settings.INSTALLED_APPS + (
    'django_whoshere',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES + (
    'django_whoshere.middleware.TrackMiddleware',)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',

    }
}
