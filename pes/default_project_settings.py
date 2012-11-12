# -*- coding:utf-8 -*-
# Django settings for pes project.
import os
from pes_local.settings import PROJECT_PATH

DEBUG = True
TEMPLATE_DEBUG = DEBUG



ADMINS = (
     ('Claude', 'contact@quinode.fr'),
)

SITE_AUTHOR = 'Quinode'
MANAGERS = ADMINS
SITE_TITLE = 'ES Agregator'


TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-FR'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'
USE_TZ = False

MEDIA_ROOT = os.path.abspath(PROJECT_PATH + '/media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(PROJECT_PATH + '/static_collected/')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.abspath(PROJECT_PATH + '/static/'),
# )

import admin_tools
ADMIN_TOOLS_PATH = os.path.dirname(os.path.abspath(admin_tools.__file__))

STATICFILES_DIRS = [
    os.path.abspath(ADMIN_TOOLS_PATH + '/media/'),
]

INTERNAL_IPS = ('127.0.0.1',)
# DEBUG_TOOLBAR_PANELS = [
#         'debug_toolbar.panels.version.VersionDebugPanel',
#         'debug_toolbar.panels.timer.TimerDebugPanel',
#         'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#         'debug_toolbar.panels.headers.HeaderDebugPanel',
#         'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#         'debug_toolbar.panels.template.TemplateDebugPanel',
#         'debug_toolbar.panels.sql.SQLDebugPanel',
#         'debug_toolbar.panels.signals.SignalDebugPanel',
#         'debug_toolbar.panels.logger.LoggingPanel',
#         #'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',
#     ]
# DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
    'pes.utils.CORSMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'pes.context_processors.current_site',
    ]


TEMPLATE_DIRS = (
    os.path.abspath(PROJECT_PATH + '/org/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #'django.test',

    # Third party tools
    'south',
    'django_rq',
    'django_push.subscriber',
    'subhub',
    'haystack',
    'haystack_fr',
    'djrdf.import_rdf',
    'pes',
    'django_extensions',
    # 'debug_toolbar'
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
       'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },

    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
       },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pes': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'djrdf': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },

    }
}



SUBHUB_MAINTENANCE_AUTO = True


# Using subhub, the hud max lease time for a subscription is 1 year. So we cannot
# avoid handling the lease time.
PUSH_LEASE_SECONDS = 365 * 86400
# Django-push. This variable is not set here because it needs to import Site
# The hud is set in the Feed class
PUSH_HUB = ''


HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
# HAYSTACK_DEFAULT_OPERATOR = 'OR'


from django.core.exceptions import ImproperlyConfigured

# import all default settings from django-rdfalchemy
try:
    from djrdf.settings import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find settings.py file from django-rdfalchemy")


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def transform_dict(dict):
    for key, value in dict.items():
        dict[key] = Namespace(value)
    return dict


RDF_NAMESPACES = {
 'ctag': u'http://commontag.org/ns#',
 'd2rq': u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#',
 'dct': u'http://purl.org/dc/terms/',
 'ess':  u'http://ns.economie-solidaire.fr/ess#',
 'event': u'http://purl.org/NET/c4dm/event.owl#',
 'foaf': u'http://xmlns.com/foaf/0.1/',
 'geofr': u'http://rdf.insee.fr/geo/',
 'gr': u'http://purl.org/goodrelations/v1#',
 'legal': u'http://www.w3.org/ns/legal#',
 'locn': u'http://www.w3.org/ns/locn#',
 'opens': u'http://rdf.opensahara.com/type/geo/',
 'org': u'http://www.w3.org/ns/org#',
 'ov': u'http://open.vocab.org/terms/',
 'person': u'http://www.w3.org/ns/person#',
 'rdfs': u'http://www.w3.org/2000/01/rdf-schema#',
 'rss': u'http://purl.org/net/rss1.1#',
 'schema': u'http://schema.org/',
 'sioc': u'http://rdfs.org/sioc/ns#',
 'skos': u'http://www.w3.org/2004/02/skos/core#',
 'skosxl': u'http://www.w3.org/2008/05/skos-xl#',
 'vcard': u'http://www.w3.org/2006/vcard/ns#',
 'vcal': u'http://www.w3.org/2002/12/cal/icaltzd#',
 'xsd': u'http://www.w3.org/2001/XMLSchema#',
 }


NS = AttributeDict(DJRDF_NS.items() +
                    transform_dict(RDF_NAMESPACES).items()
                    )

