import socket
from generate_tree import return_Tree


class Server():

    def __init__(self, port=4017):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # tells the OS to release the port after server is closed, and not hold to it.
        self.server_socket.bind(('127.0.0.1', port))
        self.server_socket.listen(1)

    def parse_message(self, message):
        try:
            parsed_message = {}
            received_message = message.split()
            parsed_message['method'] = received_message[0]
            parsed_message['path'] = received_message[1]
            parsed_message['scheme'] = received_message[2]

            return parsed_message
        except IndexError:
            raise IndexError
            #return self.http_error((400, 'Bad Request'))

    def return_uri(self, requested_path):
        return 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n %s' % requested_path

    def get(self, requested_path):
        import os
        import mimetypes
        _cwd = os.getcwd()

        if requested_path[-1] == '/':

            #requested_path = '/root/html/index.html'
            return'HTTP/1.1 200 OK\r\nContent-Type: %s\r\n\r\n%s' % ('text/html', return_Tree())

        _lookUpPath = _cwd + requested_path
        _fileType = os.path.splitext(_lookUpPath)[1]
        fileType = mimetypes.types_map[_fileType]

        try:
            with open(_lookUpPath, 'r') as _file:
               read_file= _file.read()
            return 'HTTP/1.1 200 OK\r\nContent-Type: %s\r\n\r\n%s' %(fileType, read_file)
        except IOError:
            return self.http_error((404, 'Not Found'))

    def http_error(self, error):
        return 'HTTP/1.1 %d %s\r\nContent-Type: text/plain\r\n\r\n%d %s' %(error+error)

    def do(self, _request):
        try:
            _request = self.parse_message(_request)

            if _request['method'] == 'GET' and _request['scheme'] == 'HTTP/1.1':
                return self.get(_request['path'])

            else:
                if _request['method'] != 'GET':
                    return self.http_error((405, 'Method Not Allowed'))
                if _request['scheme'] != 'HTTP/1.1':
                    return self.http_error((505, 'HTTP Version Not Supported'))
                if not _request['path']:
                    return self.http_error((404, 'Not Found'))

                return self.http_error((404, 'Not Found'))

        except IndexError:
            return self.http_error((400, 'Bad Request'))

        except:
            return self.http_error((500, 'Server Error'))

    def serve(self):

        while True:

            buffer_size = 32
            conn, client_address = self.server_socket.accept()

            response = []
            done = False
            while not done:
                recieved_message = conn.recv(buffer_size)
                if len(recieved_message) < buffer_size: # if not recieved_message did not catch the end of the request
                    done = True

                response.append(recieved_message)
            if len(response) > 1: # prevents crash when chrome checks connection
                response = ''.join(response)
                print "+"*100
                print "REQUESTED: " + str(response.split("\r\n")[0].split()[1])
                print "-"*20
                response = self.do(response)
                print "RESPONSE: " + str(response.split("\r\n")[0].split()[1:3])
                print "+"*100
                print response
                conn.sendall(response)
                conn.close()
            else:
                continue



if __name__ == "__main__":
    server = Server()
    server.serve()
