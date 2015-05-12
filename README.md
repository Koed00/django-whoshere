#Django WhosHere
A lightweight Django Admin plugin showing who's logged in from where using the cache. 
Supports [Telize](https://www.telize.com), [django-ipware](https://github.com/un33k/django-ipware), [user-agents](https://github.com/selwin/python-user-agents)  and [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/)
##Requirements

- [Django](https://www.djangoproject.com) >= 1.7

####Optional

- [user-agents](https://github.com/selwin/python-user-agents)  Adds nicer user agent formatting
- [django-ipware](https://github.com/un33k/django-ipware) More robust way of determining a users IP
- [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/)  For geolocation instead of [Telize](https://www.telize.com).

##Installation
- Make sure you have Django's [Cache](https://docs.djangoproject.com/en/1.8/topics/cache/)  backend set up.
- Install using pip: `pip install django-whoshere`
- Add `django_whoshere` to `INSTALLED_APPS` in settings.py:
```python
INSTALLED_APPS = (
    # other apps
    'django_whoshere',
)
```
- Add `django_whoshere.middelware.TrackMiddleware` to your `MIDDLEWARE_CLASSES`. 
Make sure it comes after your Authentication middleware.

```python
MIDDLEWARE_CLASSES = (
    # other middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django_whoshere.middleware.TrackMiddleware',
   # more middleware
)
```  
####Optional
- Install  [user-agents](https://github.com/selwin/python-user-agents) for nicer user agent formatting
- Install [django-ipware](https://github.com/un33k/django-ipware) for a better way to determine real ip addresses.
- Configure [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/)  or install [django-geoip-utils](https://github.com/Gidsy/django-geoip-utils)  for geo location instead of   [Telize](https://www.telize.com).

##Configuration
No configuration is needed but these settings are provided for convenience:

- `WHOSHERE_TIMEOUT = 300`
Sets the timeout for user activity. Defaults to 300 seconds.
- `WHOSHERE_LABEL = 'Active Users'`
Overrides the admin link label. Defaults to 'Active Users'
- `WHOSHERE_PREFIX = 'whoshere'`
Prefix used in cache keys. Defaults to 'whoshere'.
- `WHOSHERE_TELIZE = True`
You can set this to 'False' to turn off geolocation lookups with   [Telize](https://www.telize.com).
Is always off if GeoIp is installed.

##Geolocation
Originally this plugin started with GeoIP support only, but this means you have to install the rather large database that it comes with. 
Not a problem if you already use it for other things, but not a lightweight solution if you only use it for WhosHere.
As an alternative WhosHere uses the free  [Telize](https://www.telize.com) API over HTTPS by default to find the location of your logged in users.
This comes with some caveats:

- The [Telize](https://www.telize.com) API is [opensource](https://github.com/fcambus/telize), but you are sending users IP addresses, albeit anonymously, to a third party.
- Being a free API it can sometimes be unavailable or slow
- Your server needs HTTPS access to a remote location

You can turn off Telize lookups with `WHOSHERE_TELIZE =  False` in your `settings.py` or by installing and configuring GeoIP.

##Notes
- Middleware is kept as small as possible and only adds IP and User Agent to the cache for the current logged in user.
- No database tables are used. Instead WhosHere uses a proxy model of the User model.
- Proxy models will create migrations but do not affect your database
- Telize lookups are cached for performance

##Todo
- Add tests
- Think of other things to add

