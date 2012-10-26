# -*- coding:utf-8 -*-

PROJECT_NAME = 'pes'
SESAME_REPOSITORY_NAME = PROJECT_NAME + "Repository"
SECRET_KEY = 'c!&amp;5exu!yjh$n-!s%t4cyps-#1dd)!g=28w$^@6km3_5@l0w^0'


import os.path
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# OpenRDF configuration
OPENRDF_SERVER_NAME = 'localhost'  # default value ... to be change
OPENRDF_SERVER_PORT = '8080'       # default value when served with stock jetty conf


ROOT_URLCONF = 'pes_local.urls'
WSGI_APPLICATION = 'pes_local.wsgi.application'


from django.core.exceptions import ImproperlyConfigured

try:
    from pes.default_project_settings import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find default_project_settings.py file from pes")


# db_settings file for DATABASES, DATABASE ROUTERS and CACHE backend settings
try:
    from db_settings import *
except ImportError, exp:
    raise ImproperlyConfigured("No db_settings.py file was found")


SITE_TITLE = 'PES'



INSTALLED_APPS += (
    'pes_local',)


FEED_MODELS = ['organization', 'contact', 'exchange', 'article', 'location']
# Later, it should be
# FEED_MODELS=['organization', 'person', 'role', 'product', 'engagement', 'location', 
#               'relation', 'exchange', 'contact', 'article']




