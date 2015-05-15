from django.core.cache import cache

from django_whoshere.apps import TIMEOUT, PREFIX, get_ip


class TrackMiddleware(object):
    def __init__(self):
        pass

    @staticmethod
    def process_request(request):
        """
        Checks for authenticated user and adds ip and user-agent to the cache
        """
        if not hasattr(request, 'user'):
            return
        key = '{}:{}'.format(PREFIX, request.user.pk)
        # Add ip and user agent to cache if it's not there
        if not cache.get(key):
            cache.set(key,
                      {'ip': get_ip(request), 'agent': request.META.get('HTTP_USER_AGENT', '')},
                      TIMEOUT)
