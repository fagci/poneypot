from modules.base import Base


class Rtsp(Base):
    def handle(self):
        data = self.request.recv(1024)
        self.request.sendall('RTSP/1.0 200 OK\r\n\r\n'.encode())
