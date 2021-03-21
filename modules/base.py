from socketserver import BaseRequestHandler, ThreadingMixIn, ThreadingTCPServer


class Base(ThreadingMixIn, BaseRequestHandler):
    def __init__(self, request, client_address, server: ThreadingTCPServer):
        self.client_host, self.client_port = client_address
        print('New client', self.client_host, 'req on', server.server_address)
        super().__init__(request, client_address, server)
