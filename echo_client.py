import socket
import sys



class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
        self.client_socket.connect(('127.0.0.1', 4018))
        self.buffer_size = 32

    def send(self, message):
        # import pdb; pdb.set_trace()

        if isinstance(message, unicode):
            message = message.encode('utf-8')
        done = False
        while not done:
            self.client_socket.send(message[:self.buffer_size])
            message = message[self.buffer_size:]
            # print message

            if len(message) == 0:
                self.client_socket.shutdown(socket.SHUT_WR)
                done = True

    def receive(self):
        received_message = []
        done = False
        while not done:
            returned_message = self.client_socket.recv(self.buffer_size)

            if not returned_message:
                 done = True

            received_message.append(returned_message)

        self.client_socket.close()
        final_message = ''.join(received_message)

        return final_message

if __name__ == "__main__":
    _client = Client()
    _client.send(sys.argv[1])

    print "-"*20
    print _client.receive()



