from modules.base import Base


class Rtsp(Base):
    PROTOCOL = 'RTSP/1.0'

    def handle_each(self):
        data = self.request.recv(1024).decode().strip()

        lines = data.splitlines()
        if not lines:
            raise ValueError

        method, path, proto = lines[0].split(None, 2)

        if not proto.startswith('RTSP'):
            print('Bad proto', proto)
            raise ValueError('Bad proto')

        self.log(path)

        cseq = 1

        if len(lines) > 1 and lines[1].startswith('CSeq:'):
            _, cseq = lines[1].split(None, 1)

        headers = {'CSeq': cseq}

        if method == 'OPTIONS':
            self.respond(headers=headers)
        else:
            self.respond(404, 'Not found', headers)
