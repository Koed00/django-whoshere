from django.apps import AppConfig
from django.conf import settings

try:
    LABEL = settings.WHOSHERE_LABEL
except AttributeError:
    LABEL = 'Active Users'

try:
    TIMEOUT = settings.WHOSHERE_TIMEOUT
except AttributeError:
    TIMEOUT = 300


class SessionAdminConfig(AppConfig):
    name = 'django_whoshere'
    verbose_name = LABEL