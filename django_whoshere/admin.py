from django.contrib import admin

from django_whoshere.apps import TELIZE, GeoIP
from django_whoshere.models import UserSession


class UserSessionAdmin(admin.ModelAdmin):
    """
    Admin module for displaying active users
    """
    list_display = [
        'username',
        'ip',
        'user_agent',
        'path',
        'last_login'
    ]

    def path(self, obj):
        return '<a href="{0}" target="_blank">{0}</a>'.format(obj.path)

    def get_queryset(self, request):
        """Only show users that have tracking info"""
        qs = super(UserSessionAdmin, self).get_queryset(request)
        return qs.filter(pk__in=UserSession.active_user_ids())

    def has_add_permission(self, request, obj=None):
        """Don't allow adds"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Read only user link"""
        return False

    search_fields = ['username', 'first_name', 'last_name']
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields]

    # Add geolocation columns if possible
    if GeoIP or TELIZE:
        list_display.insert(2, 'city')
        list_display.insert(3, 'country')

    path.allow_tags = True


admin.site.register(UserSession, UserSessionAdmin)
