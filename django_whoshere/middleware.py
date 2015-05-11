from django.core.cache import cache

from django_whoshere.apps import TIMEOUT, PREFIX


def get_ip(request):
    try:
        from ipware.ip import get_real_ip
        return get_real_ip(request) or request.META.get('REMOTE_ADDR', '')
    except ImportError:
        return request.META.get('REMOTE_ADDR', '')


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
                      {'ip': get_ip(request), 'agent': request.META.get('HTTP_USER_AGENT', '')},
                      TIMEOUT)


