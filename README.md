#Django WhosHere
A simple Django Admin plugin showing who's logged in and active on your site using the cache. Supports [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/) and [user-agents](https://github.com/selwin/python-user-agents) .

##Requirements

- [Django](https://www.djangoproject.com) >= 1.7

####Optional

- [user-agents](https://github.com/selwin/python-user-agents)  Adds nicer user agent formatting

- [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/)  Looks up City and Country based on IP

- [django-geoip-utils](https://github.com/Gidsy/django-geoip-utils) The lazy way of setting up GeoIP for your project

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
- Configure [GeoIP](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/)  or just install [django-geoip-utils](https://github.com/Gidsy/django-geoip-utils)  for geo location of your users

##Configuration
No configuration is needed but these settings are provided for convenience:

- `WHOSHERE_TIMEOUT=300`
Sets the timeout for user activity. Defaults to 300 seconds.
- `WHOSHERE_LABEL='Active Users'`
Overrides the admin link label. Defaults to 'Active Users'
- `WHOSHERE_PREFIX='whoshere'`
Prefix used in cache keys. Defaults to 'whoshere'.

##Notes
- Middleware is kept as small as possible and only adds IP and User Agent to the cache for the current logged in user.
- No database tables are used. Instead WhosHere uses a proxy model of the User model.
- Proxy models will create migrations but do not affect your database

##Todo
- Add tests
- Think of other things to add

