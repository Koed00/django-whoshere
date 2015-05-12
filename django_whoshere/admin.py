from django.contrib import admin
from django_whoshere.apps import TELIZE, GeoIP

from django_whoshere.models import UserSession


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

    if GeoIP or TELIZE:
        list_display.insert(2, 'city')
        list_display.insert(3, 'country')

admin.site.register(UserSession, UserSessionAdmin)