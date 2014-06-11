import pytest

from echo_client import Client


def test_200():

    _client = Client()
    _client.send("GET / HTTP/1.1")
    assert _client.receive() == "200 OK"


def test_400():

    _client = Client()
    _client.send("GET HTTP/1.1")
    assert _client.receive() == "400 Bad Request"


def test_405():

    _client = Client()
    _client.send("PUT / HTTP/1.1")
    assert _client.receive() == "405 Method Not Allowed"
    _client = Client()
    _client.send("HEAD / HTTP/1.1")
    assert _client.receive() == "405 Method Not Allowed"


def test_505():

    _client = Client()
    _client.send("GET / HTTP/1.0")
    assert _client.receive() == "505 HTTP Version Not Supported"


def test_404():
    pass
    # cant test till there are files that cant be found
