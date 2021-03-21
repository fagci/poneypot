from modules.base import Base


class Http(Base):
    def handle(self):
        data = self.request.recv(1024)
        self.request.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode())
