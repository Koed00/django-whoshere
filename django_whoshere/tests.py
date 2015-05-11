from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, RequestFactory
from django_whoshere.apps import PREFIX

from django_whoshere.middleware import TrackMiddleware
from django_whoshere.models import UserSession


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


class WhosHereTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('WHosHereTestUser', 'WHosHereTest@requestfactory.com',
                                             'secretsecretsquirrel')
        self.key = '{}:{}'.format(PREFIX, self.user.pk)
        self.user_agent = 'Mozilla/5.0'

    def tearDown(self):
        self.user.delete()
        cache.delete(self.key)

    def test_user_request(self):
        request = self.factory.get('/', HTTP_USER_AGENT=self.user_agent)
        request.user = self.user
        TrackMiddleware.process_request(request)
        self.assertNotEqual(cache.get(self.key), None)
        active_user = UserSession.objects.first()
        self.assertEqual(active_user.ip, '127.0.0.1')
        if parse:
            self.assertEqual(active_user.user_agent.ua_string, self.user_agent)
        else:
            self.assertEqual(active_user.user_agent, self.user_agent)

        if HAS_GEOIP and GeoIP:
            self.assertEqual(active_user.city(), 'unknown')
            self.assertEqual(active_user.country(), 'unknown')

        self.assertEqual(UserSession.active_user_ids(), [1])
        self.assertEqual(UserSession.active_users()[0], self.user)
        self.assertEqual(UserSession.active_user_count(), 1)
