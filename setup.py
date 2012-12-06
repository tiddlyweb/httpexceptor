import os

from setuptools import setup, find_packages

from httpexceptor import __version__ as VERSION


DESC = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

META = {
    'name': 'httpexceptor',
    'version': VERSION,
    'long_description': DESC,
    'packages': find_packages(exclude=['test']),
    'include_package_data': False,
    'zip_safe': False,
    'install_requires': [],
    'extras_require': {
        'testing': ['pytest'],
        'coverage': ['figleaf', 'coverage']
    }
}


setup(**META)
