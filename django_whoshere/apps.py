from django.apps import AppConfig
from django.conf import settings
from django.core.cache import cache
import requests

# Sets the label name in the admin
try:
    LABEL = settings.WHOSHERE_LABEL
except AttributeError:
    LABEL = 'Active Users'

# Time for a user to be considered idle in seconds
try:
    TIMEOUT = settings.WHOSHERE_TIMEOUT
except AttributeError:
    TIMEOUT = 300

# Cache key prefix
try:
    PREFIX = settings.WHOSHERE_PREFIX
except AttributeError:
    PREFIX = 'whoshere'

# Wether or not to use Telize for ip lookups
try:
    TELIZE = settings.WOSHERE_TELIZE
except AttributeError:
    TELIZE = True

# Check if GeoIp in installed and available
try:
    from django.contrib.gis.geoip import GeoIP

    GEOIP_PATH = settings.GEOIP_PATH
except ImportError:
    GeoIP = None
except AttributeError:
    GeoIP = None

# Check if user-agents is installed
try:
    from user_agents import parse
except ImportError:
    parse = None


class SessionAdminConfig(AppConfig):
    name = 'django_whoshere'
    verbose_name = LABEL


def telize_lookup(ip):
    """
    Queries Telize.com for geolocation.
    Results are held in django cache.
    """
    key = '{}:telize:{}'.format(PREFIX, ip)
    if cache.get(key):
        return cache.get(key)
    try:
        request = requests.get('https://www.telize.com/geoip/{}'.format(ip), timeout=5)
    except requests.exceptions.Timeout:
        location = {'city': 'timeout', 'country': 'timeout'}
    except requests.exceptions.RequestException:
        location = {'city': 'error', 'country': 'error'}
    else:
        data = request.json()
        location = {'city': data.get('city', 'unknown'), 'country': data.get('country', 'unknown')}
        cache.set(key, location, TIMEOUT)
    return location


def get_ip(request):
    """
    Uses ipware to find real ip address if available.
    """
    try:
        import ipware.ip

        return ipware.ip.get_real_ip(request) or request.META.get('REMOTE_ADDR', '')
    except ImportError:
        return request.META.get('REMOTE_ADDR', '')


def get_city(ip):
    """
    Gets city location by ip either with Telize or GeoIP
    """
    if GeoIP:
        geo = GeoIP().city(str(ip))
        if geo and geo['city']:
            return geo['city']
        return 'unknown'
    return telize_lookup(ip)['city']


def get_country(ip):
    """
    Gets country location by ip either with Telize or GeoIP
    """
    if GeoIP:
        geo = GeoIP().country(str(ip))
        if geo and geo['country_name']:
            return geo['country_name']
        return 'unknown'
    return telize_lookup(ip)['country']
