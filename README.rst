Django WhosHere |image0|
========================

A lightweight Django Admin plugin showing who's logged in from where
using the cache. Supports `Telize <https://www.telize.com>`__,
`django-ipware <https://github.com/un33k/django-ipware>`__,
`user-agents <https://github.com/selwin/python-user-agents>`__ and
`GeoIP <https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/>`__

Requirements
------------

-  `Django <https://www.djangoproject.com>`__ >= 1.7
-  `requests <https://github.com/kennethreitz/requests>`__

Optional
^^^^^^^^

-  `user-agents <https://github.com/selwin/python-user-agents>`__ Adds
   nicer user agent formatting
-  `django-ipware <https://github.com/un33k/django-ipware>`__ More
   robust way of determining a users IP
-  `GeoIP <https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/>`__
   For geolocation instead of `Telize <https://www.telize.com>`__.

Installation
------------

-  Make sure you have Django's
   `Cache <https://docs.djangoproject.com/en/1.8/topics/cache/>`__
   backend set up.
-  Install using pip: ``pip install django-whoshere``
-  Add ``django_whoshere`` to ``INSTALLED_APPS`` in settings.py:

   .. code:: python

       INSTALLED_APPS = (
           # other apps
           'django_whoshere',
       )

-  Add ``django_whoshere.middelware.TrackMiddleware`` to your
   ``MIDDLEWARE_CLASSES``. Make sure it comes after your Authentication
   middleware.

.. code:: python

    MIDDLEWARE_CLASSES = (
        # other middleware
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django_whoshere.middleware.TrackMiddleware',
       # more middleware
    )

Optional
^^^^^^^^

-  Install
   `user-agents <https://github.com/selwin/python-user-agents>`__ for
   nicer user agent formatting
-  Install `django-ipware <https://github.com/un33k/django-ipware>`__
   for a better way to determine real ip addresses.
-  Configure
   `GeoIP <https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/>`__
   or install
   `django-geoip-utils <https://github.com/Gidsy/django-geoip-utils>`__
   for geo location instead of `Telize <https://www.telize.com>`__.

Configuration
-------------

No configuration is needed but these settings are provided for
convenience:

-  ``WHOSHERE_TIMEOUT = 300`` Sets the timeout for user activity.
   Defaults to 300 seconds.
-  ``WHOSHERE_LABEL = 'Active Users'`` Overrides the admin link label.
   Defaults to 'Active Users'
-  ``WHOSHERE_PREFIX = 'whoshere'`` Prefix used in cache keys. Defaults
   to 'whoshere'.
-  ``WHOSHERE_TELIZE = True`` You can set this to 'False' to turn off
   geolocation lookups with `Telize <https://www.telize.com>`__. Is
   always off if GeoIp is installed.

Template tags
-------------

Besides the admin interface, WhosHere's functions are also available as
template tags: \`\`\`html+django {% load whoshere %}

There are now {% active\_user\_count %} users logged in.

{% active\_users as users %}

.. raw:: html

   <ul>

{% for user in users %}

.. raw:: html

   <li>

{{ user.username }} ({{ user.email }})

.. raw:: html

   </li>

{% endfor %}

.. raw:: html

   </ul>

   <p>

Your IP address is {% your\_ip %}

.. raw:: html

   </p>
   <p>

Your browser and platform is {% your\_agent %}

.. raw:: html

   </p>
   <p>

You live in {% your\_city %}, {% your\_country %}

.. raw:: html

   </p>

\`\`\`

Geolocation
-----------

Originally this plugin started with GeoIP support only, but this means
you have to install the rather large database that it comes with. Not a
problem if you already use it for other things, but not a lightweight
solution if you only use it for WhosHere. As an alternative WhosHere
uses the free `Telize <https://www.telize.com>`__ API over HTTPS by
default to find the location of your logged in users. This comes with
some caveats:

-  The `Telize <https://www.telize.com>`__ API is
   `opensource <https://github.com/fcambus/telize>`__, but you are
   sending users IP addresses, albeit anonymously, to a third party.
-  Being a free API it can sometimes be unavailable or slow
-  Your server needs HTTPS access to a remote location

You can turn off Telize lookups with ``WHOSHERE_TELIZE =  False`` in
your ``settings.py`` or by installing and configuring GeoIP.

Notes
-----

-  Middleware is kept as small as possible and only adds IP and User
   Agent to the cache for the current logged in user.
-  No database tables are used. Instead WhosHere uses a proxy model of
   the User model.
-  Proxy models will create migrations but do not affect your database
-  Telize lookups are cached for performance
-  Using the excellent requests library for better SSL support

Todo
----

-  Add tests
-  Think of other things to add

.. |image0| image:: https://travis-ci.org/Koed00/django-whoshere.svg?branch=master
