from django.core.cache import cache
from django_whoshere.apps import TIMEOUT, PREFIX


class TrackMiddleware():
    def __init__(self):
        pass

    @staticmethod
    def process_request(request):
        if not hasattr(request, 'user'):
            return
        key = '{}:{}'.format(PREFIX, request.user.pk)
        if not cache.get(key):
            cache.set(key,
                      {'ip': request.META.get('REMOTE_ADDR', ''), 'agent': request.META.get('HTTP_USER_AGENT', '')},
                      TIMEOUT)

