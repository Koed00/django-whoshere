from django.core.cache import cache

from django_whoshere.apps import TIMEOUT, PREFIX


def get_ip(request):
    """
    Uses ipware to find real ip address if available.
    """
    try:
        import ipware.ip

        return ipware.ip.get_real_ip(request) or request.META.get('REMOTE_ADDR', '')
    except ImportError:
        return request.META.get('REMOTE_ADDR', '')


class TrackMiddleware:
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
