import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-whoshere',
    version='0.1.6',
    author='Ilan Steemers',
    author_email='koed00@gmail.com',
    packages=['django_whoshere'],
    url='https://github.com/koed00/django-whoshere',
    license='MIT',
    description='Lightweight Django Admin plugin to see who is logged in and active. Supports Telize.com, GeoIp , user-agents and django-ipware.',
    long_description=README,
    include_package_data=True,
    install_requires=['django>=1.7', 'requests'],
    test_suite='django_whoshere.tests.runtests.runtests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)