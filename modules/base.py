from socketserver import BaseRequestHandler, ThreadingMixIn, ThreadingTCPServer
from pathlib import Path
import os
from datetime import datetime


class Base(ThreadingMixIn, BaseRequestHandler):
    PROTOCOL = 'HTTP/1.1'
    logfile = None

    def __init__(self, request, client_address, server: ThreadingTCPServer):
        self.client_host, self.client_port = client_address
        if Base.logfile is None:
            class_name = self.__class__.__name__
            logname = '%s.log' % class_name.lower()
            c_path = Path(os.path.dirname(os.path.abspath(__file__)))
            Base.logfile = c_path / '..' / 'log' / logname
        super().__init__(request, client_address, server)

    def respond(self, code: int = 200, msg: str = 'OK', headers: dict = {}, body: str = ''):
        headers_str = '\r\n'.join('%s: %s' % v for v in headers.items())

        if headers_str:
            headers_str += '\r\n'

        if body:
            body += '\r\n\r\n'

        self.request.sendall(((
            '%s %s %s\r\n'
            '%s'
            '\r\n'
            '%s'
        ) % (
            self.PROTOCOL, code, msg,
            headers_str,
            body
        )).encode())

    def log(self, *args):
        dt = datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
        with self.logfile.open('a') as f:
            line = ' '.join([
                dt,
                self.client_host,
                str(self.server.server_address[1]),
                *args
            ])
            f.write(line + '\n')
            print(line)

    def handle_each(self):
        raise NotImplementedError

    def handle(self):
        while True:
            try:
                if self.handle_each() is False:
                    self.finish()
                    return
            except KeyboardInterrupt:
                self.server.shutdown()
                return
            except Exception as e:
                print(e)
                self.finish()
                return
