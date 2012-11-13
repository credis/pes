#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

VERSION = __import__('pes').__version__

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pes',
    version = VERSION,
    description = 'A basis for ess agreator',
    packages = ['pes',
                'pes.article',
                'pes.bin',
                'pes.exchange',
                'pes.geo',
                'pes.management',
                'pes.management.commands',
                'pes.org',
                'pes.tag',
                'pes.templatetags',
                'pes.thess',
               ],
    include_package_data = True,
    author = 'Cooperative Quinode',
    author_email = 'contact@quinode.fr',
    license = 'BSD',
    zip_safe = False,
    install_requires = ['south', 'django==1.4.2', 
                        #'sorl-thumbnail==11.09',
                        #'django-extensions==0.8',  # waiting for new Pypi version with our 12/09/12 commit
                        #'django-admin-tools==0.4.1', # for 1.4 : waiting for merging of https://bitbucket.org/psyton/django-admin-tools
                        #'django-haystack==1.2.6', # github dev version needed
                        #'djangoembed==0.1.1', # Pypi: bad version, we use: https://github.com/ericflo/django-oembed
                        ],
    long_description = open('README.rst').read(),
    url = 'https://github.com/quinode/pes/',
    download_url = 'https://github.com/quinode/pes/tarball/master',
    scripts = [
        'pes/bin/pes-admin.py',
        'pes/bin/runinenv.sh'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Natural Language :: English',
        'Natural Language :: French',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],

)
