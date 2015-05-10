from importlib import import_module

from django.conf import settings
from django.contrib import admin

from django.contrib.gis.geoip import HAS_GEOIP

from django_whoshere.models import UserSession


try:
    from user_agents import parse
except ImportError:
    parse = None
if HAS_GEOIP:
    try:
        GEOIP_PATH = settings.GEOIP_PATH
    except AttributeError:
        GEOIP_PATH = None

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class UserSessionAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'ip',
        'user_agent',
        'last_login'
    ]

    def get_queryset(self, request):
        qs = super(UserSessionAdmin, self).get_queryset(request)
        return qs.filter(pk__in=UserSession.active_user_ids())

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields]

    if HAS_GEOIP and GEOIP_PATH:
        list_display.insert(3, 'city')
        list_display.insert(4, 'country')

admin.site.register(UserSession, UserSessionAdmin)