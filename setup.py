import os

from setuptools import setup, find_packages

from httpexceptor import __version__ as VERSION, __author__ as AUTHOR


DESC = open(os.path.join(os.path.dirname(__file__), 'README')).read()

CLASSIFIERS = """
Environment :: Web Environment
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware
""".strip().splitlines()

META = {
    'name': 'httpexceptor',
    'url': 'https://github.com/tiddlyweb/httpexceptor',
    'version': VERSION,
    'description': 'WSGI middleware to handle HTTP responses using exceptions',
    'long_description': DESC,
    'classifiers': CLASSIFIERS,
    'license': 'LICENSE',
    'author': AUTHOR,
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


if __name__ == '__main__':
    setup(**META)
