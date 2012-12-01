"""
lightweight WSGI middleware to handle common HTTP responses using exceptions

provides a group of exception classes representing non-2xx HTTP statuses, along
with a WSGI middleware to turn the exceptions into proper HTTP headers

originally extracted from [TiddlyWeb](http://tiddlyweb.com)
"""

import sys
import traceback
import logging


class HTTPException(Exception):
    """
    base class of an HTTP exception
    """

    status = ''

    def headers(self):
        return [('Content-Type', 'text/plain; charset=UTF-8')]

    def output(self):
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

    status = __doc__

    def headers(self):
        return [('Location', '%s' % self)]

    def output(self):
        return ['']


class HTTP303(HTTP302):
    """303 See Other"""

    status = __doc__


class HTTP304(HTTPException):
    """304 Not Modified"""

    status = __doc__

    def headers(self):
        return [('Etag', '%s' % self)]

    def output(self):
        return ['']


class HTTP400(HTTPException):
    """400 Bad Request"""

    status = __doc__


class HTTP401(HTTPException):
    """401 Unauthorized"""

    status = __doc__

    def headers(self):
        return [('WWW-Authenticate', '%s' % self)]

    def output(self):
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
    """415 Unsupported"""

    status = __doc__


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
            start_response(exc.status, exc.headers(), exc_info)
            return exc.output()
        except:
            etype, value, traceb = sys.exc_info()
            exception_text = ''.join(traceback.format_exception(
                etype, value, traceb, None))

            # use both the web server's and the application's logging mechanisms
            print >> environ['wsgi.errors'], exception_text
            logging.warn(exception_text)

            start_response('500 server error',
                    [('Content-Type', 'text/plain')], sys.exc_info())
            return [exception_text]
