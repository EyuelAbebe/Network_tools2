import pytest

from echo_client import Client


def test_200():

    _client = Client()
    _client.send("GET / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n200 OK'


def test_400():

    _client = Client()
    _client.send("GET HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\n400 Bad Request'


def test_405():

    _client = Client()
    _client.send("PUT / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\n405 Method Not Allowed'
    _client = Client()
    _client.send("HEAD / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\n405 Method Not Allowed'


def test_505():

    _client = Client()
    _client.send("GET / HTTP/1.0")
    assert _client.receive() == 'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\n\r\n505 HTTP Version Not Supported'


def test_404():
    pass
    # cant test till there are files that cant be found
