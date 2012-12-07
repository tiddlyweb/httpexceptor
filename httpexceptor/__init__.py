"""
lightweight WSGI middleware to handle common HTTP responses using exceptions

provides a group of exception classes representing non-2xx HTTP statuses, along
with a WSGI middleware to turn the exceptions into proper HTTP headers

originally extracted from [TiddlyWeb](http://tiddlyweb.com)
"""

import sys
import traceback
import logging


__version__ = '1.1.0'
__author__ = 'Chris Dent'
__copyright__ = 'Copyright UnaMesa Association 2012'
__contributors__ = ['FND']
__license__ = 'BSD'


class HTTPExceptor(object):
    """
    WSGI middleware to trap exceptions, turning them into the corresponding
    HTTP response
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response, exc_info=None):
        try:
            return self.application(environ, start_response)
        except HTTPException, exc:
            # read status code from exception class's docstring
            start_response(exc.status, exc.headers(), exc_info)
            return exc.body()
        except:
            exc_info = sys.exc_info()
            exception_text = ''.join(traceback.format_exception(*exc_info))

            # use the web server's and the application's logging mechanisms
            print >> environ['wsgi.errors'], exception_text
            logging.warn(exception_text)

            start_response('500 Internal Server Error',
                    [('Content-Type', 'text/plain; charset=UTF-8')], exc_info)
            return [exception_text]


class HTTPException(Exception):
    """
    base class of an HTTP exception
    """

    status = None

    def headers(self):
        return [('Content-Type', 'text/plain; charset=UTF-8')]

    def body(self):
        if not hasattr(self, 'args'):
            self.args = ('%s' % self,)
        output = []
        for arg in self.args:
            if isinstance(arg, unicode):
                arg = arg.encode('utf-8')
            output.append('%s' % arg)
        status_code = self.status.split(" ")[0]
        return ['%s: %s' % (status_code, ' '.join(output))]


class HTTP302(HTTPException):
    """302 Found"""

    status = __doc__

    def headers(self):
        return [('Location', '%s' % self)]

    def body(self):
        return ['']


class HTTP303(HTTP302):
    """303 See Other"""

    status = __doc__


class HTTP304(HTTPException):
    """304 Not Modified"""

    status = __doc__

    def headers(self):
        return [('ETag', '%s' % self)]

    def body(self):
        return ['']


class HTTP400(HTTPException):
    """400 Bad Request"""

    status = __doc__


class HTTP401(HTTPException):
    """401 Unauthorized"""

    status = __doc__

    def headers(self):
        return [('WWW-Authenticate', '%s' % self)]

    def body(self):
        return ['']


class HTTP403(HTTPException):
    """403 Forbidden"""

    status = __doc__


class HTTP404(HTTPException):
    """404 Not Found"""

    status = __doc__


class HTTP409(HTTPException):
    """409 Conflict"""

    status = __doc__


class HTTP412(HTTPException):
    """412 Precondition Failed"""

    status = __doc__


class HTTP415(HTTPException):
    """415 Unsupported Media Type"""

    status = __doc__
