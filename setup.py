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
        'Django~=4.2',
        'django-userservice~=3.1',
        'django-storages[google]',
        'uw-memcached-clients~=1.0',
        'UW-RestClients-Core~=1.4',
        'UW-RestClients-GWS~=2.3',
        'UW-RestClients-PWS~=2.1',
        'UW-RestClients-Catalyst~=1.1',
        'UW-RestClients-Django-Utils~=2.3',
        'UW-Django-SAML2~=1.7',
        'Django-SupportTools~=3.6',
        'Django-Persistent-Message',
    ],
    license='Apache License, Version 2.0',
    description='UW application that supports catalyst',
    long_description=README,
    url='https://github.com/uw-it-aca/catalyst-utils',
    author="UW-IT AXDD",
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
