from modules.base import Base


class Http(Base):
    def handle_each(self):
        data = self.request.recv(1024).decode()
        lines = data.splitlines()

        if not lines:
            raise ValueError

        first_line = lines[0]

        if ' HTTP/' not in first_line:
            self.respond(400, 'Bad request')
            raise ValueError('Bad request')

        method, url, protocol = first_line.split(None, 2)

        self.log(method, url, protocol)

        self.respond()
        return False
