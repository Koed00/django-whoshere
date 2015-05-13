from django.contrib.auth.models import User
from django.core.cache import cache

from django_whoshere.apps import PREFIX, GeoIP, parse, telize_lookup


class UserSession(User):
    """
    A proxy model to auth.models.User
    """

    @property
    def track(self):
        """Get the tracking info from the cache"""
        return cache.get(self.key)

    @property
    def key(self):
        """
        Cache key. Redis compatible format.
        Can be configured with WHOSHERE_PREFIX
        """
        return '{}:{}'.format(PREFIX, self.pk)

    @property
    def ip(self):
        """Raw ip from the cache"""
        if self.track:
            return self.track['ip']

    @property
    def user_agent(self):
        """
        Returns raw user agent string or parsed with user-agents if available
        """
        if self.track:
            if parse:
                return parse(self.track['agent'])
            return self.track['agent']

    def city(self):
        """ Return city name using Telize or Geoip."""
        if GeoIP:
            geo = GeoIP().city(str(self.ip))
            if geo and geo['city']:
                return geo['city']
            return 'unknown'
        return telize_lookup(self.ip)['city']

    def country(self, ):
        """
        Returns country name using Telize or GeoIP
        """
        if GeoIP:
            geo = GeoIP().city(str(self.ip))
            if geo and geo['country_name']:
                return geo['country_name']
            return 'unknown'
        return telize_lookup(self.ip)['country']

    @staticmethod
    def active_user_ids():
        """
        returns a list of currently tracked user id's
        """
        return [user.id for user in UserSession.objects.all() if user.track]

    @staticmethod
    def active_users():
        """
        returns the currently tracked users
        """
        return [user for user in UserSession.objects.all() if user.track]

    @staticmethod
    def active_user_count():
        """
        returns the number of currently trackers users
        """
        return len(UserSession.active_user_ids())

    class Meta:
        proxy = True
