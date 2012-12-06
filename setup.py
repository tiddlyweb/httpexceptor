import os

import httpexceptor

from setuptools import setup, find_packages


DESC = open(os.path.join(os.path.dirname(__file__), 'README')).read()

META = {
    'name': 'httpexceptor',
    'url': 'http://pypi.python.org/pypi/httpexceptor',
    'version': httpexceptor.__version__,
    'description': 'lightweight WSGI middleware to handle common HTTP responses using exceptions',
    'long_description': DESC,
    'license': 'LICENSE',
    'author': httpexceptor.__author__,
    'author_email': 'cdent@peermore.com',
    'maintainer': 'FND',
    'packages': find_packages(exclude=['test']),
    'platforms': 'Posix; MacOS X; Windows',
    'include_package_data': False,
    'zip_safe': False,
    'install_requires': [],
    'extras_require': {
        'testing': ['pytest'],
        'coverage': ['figleaf', 'coverage']
    }
}


setup(**META)
