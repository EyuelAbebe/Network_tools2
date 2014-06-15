import pytest

from echo_client import Client
from generate_tree import return_Tree


def test_200():

    _client = Client()
    _client.send("GET / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n%s' %return_Tree()


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

def test_500():

    _client = Client()
    _client.send("GET /adsfasdfasd HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\n\r\n500 Server Error'

def test_505():

    _client = Client()
    _client.send("GET / HTTP/1.0")
    assert _client.receive() == 'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain\r\n\r\n505 HTTP Version Not Supported'


def test_404():
    _client = Client()
    _client.send("GET /root/cpp.jpeg HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found'
