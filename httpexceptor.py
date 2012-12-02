"""
lightweight WSGI middleware to handle common HTTP responses using exceptions

provides a group of exception classes representing non-2xx HTTP statuses, along
with a WSGI middleware to turn the exceptions into proper HTTP headers

originally extracted from [TiddlyWeb](http://tiddlyweb.com)
"""

import sys
import traceback
import logging
import httplib


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
            exc.status = int(exc.__class__.__doc__.split(' ')[0])
            start_response('%s %s' % (exc.status, httplib.responses[exc.status]),
                    exc.headers(), exc_info)
            return exc.body()
        except:
            exc_info = sys.exc_info()
            exception_text = ''.join(traceback.format_exception(*exc_info))

            # use both the web server's and the application's logging mechanisms
            print >> environ['wsgi.errors'], exception_text
            logging.warn(exception_text)

            start_response('500 %s' % httplib.responses[500],
                    [('Content-Type', 'text/plain; charset=UTF-8')], exc_info)
            return [exception_text]


class HTTPException(Exception):
    """
    base class of an HTTP exception
    """

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
        return ['%s: %s' % (self.status, ' '.join(output))]


class HTTP302(HTTPException):
    """302 Found"""

    def headers(self):
        return [('Location', '%s' % self)]

    def body(self):
        return ['']


class HTTP303(HTTP302):
    """303 See Other"""


class HTTP304(HTTPException):
    """304 Not Modified"""

    def headers(self):
        return [('ETag', '%s' % self)]

    def body(self):
        return ['']


class HTTP400(HTTPException):
    """400 Bad Request"""


class HTTP401(HTTPException):
    """401 Unauthorized"""

    def headers(self):
        return [('WWW-Authenticate', '%s' % self)]

    def body(self):
        return ['']


class HTTP403(HTTPException):
    """403 Forbidden"""


class HTTP404(HTTPException):
    """404 Not Found"""


class HTTP409(HTTPException):
    """409 Conflict"""


class HTTP412(HTTPException):
    """412 Precondition Failed"""


class HTTP415(HTTPException):
    """415 Unsupported"""
