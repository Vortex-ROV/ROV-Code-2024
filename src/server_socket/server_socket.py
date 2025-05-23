import socket


class ServerSocket:
    def __init__(self, port: int):
        self.__welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__welcoming_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__welcoming_socket.bind(("192.168.33.1", port))
        self.__welcoming_socket.listen()

    def accept(self):
        print("waiting for client")
        self.__client_socket, _ = self.__welcoming_socket.accept()
        self.__client_socket.setblocking(False)
        print("connected to client")

    def receive(self, buffer_size: int):
        try:
            received = self.__client_socket.recv(buffer_size)
            if received is not None and len(received) != 0:
                return received
            raise socket.error
        except socket.error as e:
            # handle receive not ready
            if e.errno == 11:
                return
            print(e)
            self.__client_socket.close()
            self.accept()

    def send(self, data: bytes):
        try:
            self.__client_socket.send(data)
        except socket.error as e:
            print(e)
            self.__client_socket.close()
            self.accept()
        except AttributeError as e:
            pass

    def __del__(self):
        self.__welcoming_socket.close()
        self.__client_socket.close()
    # def closedSocket(self): #try it 29/4/2024 if not working remove it / to handle if socket disconnected stop rov until its connected again 
    #     return self.closed

if  __name__ == '__main__' :
    ServerSocket(4096)