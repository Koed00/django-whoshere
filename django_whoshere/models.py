from django.contrib.auth.models import User
from django.core.cache import cache

from django_whoshere.apps import PREFIX, GeoIP, parse, telize_lookup


class UserSession(User):
    @property
    def track(self):
        return cache.get(self.key)

    @property
    def key(self):
        return '{}:{}'.format(PREFIX, self.pk)

    @property
    def ip(self):
        if self.track:
            return self.track['ip']

    @property
    def user_agent(self):
        if self.track:
            if parse:
                return parse(self.track['agent'])
            return self.track['agent']

    def city(self):
        if GeoIP:
            geo = GeoIP().city(str(self.ip))
            if geo and geo['city']:
                return geo['city']
            return 'unknown'
        return telize_lookup(self.ip)['city']

    def country(self, ):
        if GeoIP:
            geo = GeoIP().city(str(self.ip))
            if geo and geo['country_name']:
                return geo['country_name']
            return 'unknown'
        return telize_lookup(self.ip)['country']

    @staticmethod
    def active_user_ids():
        return [user.id for user in UserSession.objects.all() if user.track]

    @staticmethod
    def active_users():
        return [user for user in UserSession.objects.all() if user.track]

    @staticmethod
    def active_user_count():
        return len(UserSession.active_user_ids())

    class Meta:
        proxy = True