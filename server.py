

def parse_message(message):
    try:
        parsed_message = {}
        received_message = message.split()
        parsed_message['method'] = received_message[0]
        parsed_message['path'] = received_message[1]
        parsed_message['scheme'] = received_message[2]

        return parsed_message
    except IndexError:
        raise IndexError


def return_uri(requested_path):
    return 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n %s' % requested_path


def get(requested_path):
    import os
    import mimetypes
    _cwd = os.getcwd()

    if requested_path == '/':
        requested_path = '/root/html/index.html'

    _lookUpPath = _cwd + requested_path
    _fileType = os.path.splitext(_lookUpPath)[1]
    fileType = mimetypes.types_map[_fileType]

    try:
        with open(_lookUpPath, 'r') as _file:
           read_file= _file.read()
        return 'HTTP/1.1 200 OK\r\nContent-Type: %s\r\n\r\n%s' %(fileType, read_file)
    except IOError:
        return http_error((404, 'Not Found'))


def http_error(error):
    return 'HTTP/1.1 %d %s\r\nContent-Type: text/plain\r\n\r\n%d %s' %(error+error)


def do(_request):
    try:
        _request = parse_message(_request)

        if _request['method'] == 'GET' and _request['scheme'] == 'HTTP/1.1':
            return get(_request['path'])

        else:
            if _request['method'] != 'GET':
                return http_error((405, 'Method Not Allowed'))
            if _request['scheme'] != 'HTTP/1.1':
                return http_error((505, 'HTTP Version Not Supported'))
            if not _request['path']:
                return http_error((404, 'Not Found'))

            return http_error((404, 'Not Found'))

    except IndexError:
        return http_error((400, 'Bad Request'))

    except:
        return http_error((500, 'Server Error'))


def serve(socket, address):

    received_message = []
    buffersize = 32
    done = False
    while not done:
        data = socket.recv(buffersize)
        received_message.append(data)

        if len(data) < buffersize:
            done = True

    received_message = ''.join(received_message)

    print '+'*50
    print received_message
    print '-'*40
    response = do(received_message)
    print response
    print '+'*50
    socket.sendall(response)
    socket.close()


if __name__ == "__main__":
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 4018), serve )
    server.serve_forever()
