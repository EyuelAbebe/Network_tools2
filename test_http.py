
from echo_client import Client


def test_200():

    _client = Client()
    _client.send("GET / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 200 OK\r\nContent-Type: text/html'


def test_400():

    _client = Client()
    _client.send("GET HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain'


def test_405():

    _client = Client()
    _client.send("PUT / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain'
    _client = Client()
    _client.send("HEAD / HTTP/1.1")
    assert _client.receive() == 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain'


def test_505():

    _client = Client()
    _client.send("GET / HTTP/1.0")
    assert _client.receive() == 'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain'

def test_404():

    _client = Client()
    _client.send("GET /asdkfa;kdfjas;dkf HTTP/1.0")
    assert _client.receive() == 'HTTP/1.1 505 HTTP Version Not Supported\r\nContent-Type: text/plain'
