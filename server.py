import socket


class Server():

    def __init__(self, port = 4016):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
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
            return self.http_error((400, 'Bad Request'))

    def return_uri(self, requested_path):
        return 'HTTP/1.1 200 OK Content-Type: text/plain\r\n %s' %requested_path

    def get(self):
        #return 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n200 OK'
        return "200 OK"

    def http_error(self, error):
        #return 'HTTP/1.1 %d %s Content-Type: text/plain\r\n%d %s'%(error+error)
        return "%d %s"%error

    def do(self, _request):
        try:
            _request = self.parse_message(_request)

            if type(_request) != dict:
                return _request
            else:
                if _request['method'] == 'GET' and _request['scheme'] == 'HTTP/1.1':
                    return self.get()

                else:
                    if _request['method'] != 'GET':
                        return self.http_error((405, 'Method Not Allowed'))
                    if _request['scheme'] != 'HTTP/1.1':
                        return self.http_error((505, 'HTTP Version Not Supported'))
                    if not _request['path']:
                        return self.http_error((404, 'Not Found'))

                    return self.http_error((404, 'Not Found'))
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

            response = ''.join(response)

            print response
            #import pdb; pdb.set_trace()
            response = self.do(response)
            print response

            conn.sendall(response)
            conn.close()


if __name__ == "__main__":
    server = Server()
    server.serve()
