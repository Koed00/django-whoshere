from django.contrib.auth.models import User
from django.core.cache import cache

try:
    from user_agents import parse
except ImportError:
    parse = None
from django.contrib.gis.geoip import HAS_GEOIP

if HAS_GEOIP:
    try:
        from django.contrib.gis.geoip import GeoIP
    except ImportError:
        GeoIP = None


class UserSession(User):
    @property
    def track(self):
        return cache.get(self.key)

    @property
    def key(self):
        return 'whoshere:{}'.format(self.pk)

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
        geo = GeoIP().city(str(self.ip))
        if geo and geo['city']:
            return geo['city']
        return 'unknown'

    def country(self, ):
        geo = GeoIP().city(str(self.ip))
        if geo and geo['country_name']:
            return geo['country_name']
        return 'unknown'

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