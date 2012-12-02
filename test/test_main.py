import httpexceptor

from StringIO import StringIO


def mock_response(error=None, message=None):
    responses = []
    environ = { 'wsgi.errors': StringIO() }

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

    assert status == '200 OK'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain'
    assert body == ['no errors']


def test_302():
    status, headers, body = mock_response(302, 'http://example.org')

    assert status == '302 Found'
    assert len(headers) == 1
    assert headers['Location'] == 'http://example.org'
    assert body == ['']


def test_303():
    status, headers, body = mock_response(303, 'http://example.org')

    assert status == '303 See Other'
    assert len(headers) == 1
    assert headers['Location'] == 'http://example.org'
    assert body == ['']


def test_304():
    status, headers, body = mock_response(304, '123abc')

    assert status == '304 Not Modified'
    assert len(headers) == 1
    assert headers['ETag'] == '123abc'
    assert body == ['']


def test_400():
    status, headers, body = mock_response(400)

    assert status == '400 Bad Request'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['400: error message']


def test_401():
    status, headers, body = mock_response(401, 'login')

    assert status == '401 Unauthorized'
    assert len(headers) == 1
    assert headers['WWW-Authenticate'] == 'login'
    assert body == ['']


def test_403():
    status, headers, body = mock_response(403)

    assert status == '403 Forbidden'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['403: error message']


def test_404():
    status, headers, body = mock_response(404)

    assert status == '404 Not Found'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['404: error message']


def test_409():
    status, headers, body = mock_response(409)

    assert status == '409 Conflict'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['409: error message']


def test_412():
    status, headers, body = mock_response(412)

    assert status == '412 Precondition Failed'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['412: error message']


def test_415():
    status, headers, body = mock_response(415)

    assert status == '415 Unsupported Media Type'
    assert len(headers) == 1
    assert headers['Content-Type'] == 'text/plain; charset=UTF-8'
    assert body == ['415: error message']
