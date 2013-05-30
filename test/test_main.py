import httplib

import httpexceptor

from StringIO import StringIO


def mock_response(error=None, message=None):
    responses = []
    environ = {'wsgi.errors': StringIO()}

    def start_response_mock(status, headers, exc_info=None):
        responses.append((status, dict(headers)))

    def app(environ, start_response):
        if error:
            exception_class = getattr(httpexceptor, 'HTTP%s' % error)
            raise exception_class(message or 'error message')
        else:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['no errors']

    # register middleware
    app = httpexceptor.HTTPExceptor(app)

    body = app(environ, start_response_mock)
    return responses[0][0], responses[0][1], body


def test_no_errors():
    status, headers, body = mock_response()

    assert status == _status(200)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain'
    assert body == ['no errors']


def test_302():
    status, headers, body = mock_response(302, 'http://example.org')

    assert status == _status(302)
    assert len(headers) == 1
    assert headers['Location'] == 'http://example.org'
    assert body == ['']


def test_303():
    status, headers, body = mock_response(303, 'http://example.org')

    assert status == _status(303)
    assert len(headers) == 1
    assert headers['Location'] == 'http://example.org'
    assert body == ['']


def test_304():
    status, headers, body = mock_response(304, '123abc')

    assert status == _status(304)
    assert len(headers) == 1
    assert headers['etag'] == '123abc'
    assert body == ['']


def test_304_httpbis():
    exception = httpexceptor.HTTP304(etag='123abc', vary='accept',
            cache_control='no-cache', last_modified='bad date',
            expires='bad time', content_location='http://example.com')

    assert exception.status == '304 Not Modified'
    assert exception.body() == ['']
    headers = {header[0]: header[1] for header in exception.headers()}
    assert len(headers) == 6
    assert headers['etag'] == '123abc'
    assert headers['vary'] == 'accept'
    assert headers['cache-control'] == 'no-cache'
    assert headers['last-modified'] == 'bad date'
    assert headers['expires'] == 'bad time'
    assert headers['content-location'] == 'http://example.com'

    exception = httpexceptor.HTTP304(etag='123abc')

    assert exception.status == '304 Not Modified'
    assert exception.body() == ['']
    headers = {header[0]: header[1] for header in exception.headers()}
    assert len(headers) == 1
    assert headers['etag'] == '123abc'
    assert 'vary' not in headers
    assert 'cache-control' not in headers
    assert 'last-modified' not in headers
    assert 'expires' not in headers
    assert 'content-location' not in headers


def test_400():
    status, headers, body = mock_response(400)

    assert status == _status(400)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['400 Bad Request: error message']


def test_401():
    status, headers, body = mock_response(401, 'login')

    assert status == _status(401)
    assert len(headers) == 1
    assert headers['WWW-Authenticate'] == 'login'
    assert body == ['']


def test_403():
    status, headers, body = mock_response(403)

    assert status == _status(403)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['403 Forbidden: error message']


def test_404():
    status, headers, body = mock_response(404)

    assert status == _status(404)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['404 Not Found: error message']


def test_409():
    status, headers, body = mock_response(409)

    assert status == _status(409)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['409 Conflict: error message']


def test_412():
    status, headers, body = mock_response(412)

    assert status == _status(412)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['412 Precondition Failed: error message']


def test_415():
    status, headers, body = mock_response(415)

    assert status == _status(415)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['415 Unsupported Media Type: error message']


def test_500():
    status, headers, body = mock_response(999, "fail")

    assert status == _status(500)
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert len(body) == 1
    assert body[0].startswith("Traceback ")


def _status(code):
    return '%s %s' % (code, httplib.responses[code])
