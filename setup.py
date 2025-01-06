#!/usr/bin/env python

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/catalyst-utils>`_.
"""

version_path = 'catalyst_utils/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='catalyst-utils',
    version=VERSION,
    packages=['catalyst_utils'],
    include_package_data=True,
    install_requires=[
        'django~=4.2',
        'django-userservice~=3.2',
        'django-storages[google]',
        'uw-memcached-clients~=1.0',
        'uw-restclients-core~=1.4',
        'uw-restclients-gws~=2.3',
        'uw-restclients-pws~=2.1',
        'uw-restclients-catalyst~=1.1',
        'uw-restclients-django-utils~=2.3',
        'uw-django-saml2~=1.8',
        'django-supporttools~=3.6',
        'django-persistent-message~=1.3'
    ],
    license='Apache License, Version 2.0',
    description='UW application that supports catalyst',
    long_description=README,
    url='https://github.com/uw-it-aca/catalyst-utils',
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
