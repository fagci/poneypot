#!/usr/bin/env python3
from configparser import ConfigParser
from socketserver import ThreadingTCPServer
from threading import Thread
from time import sleep


def camel_cased(s):
    return ''.join(p.title() for p in s.split('_'))


def main():
    cfg_parser = ConfigParser()
    cfg_parser.read('config.ini')

    modules = cfg_parser.sections()

    servers = []
    threads = []

    for module_name in modules:
        m_cfg = cfg_parser[module_name]

        if not m_cfg.get('enabled'):
            continue

        try:
            imported = __import__('modules.%s' % module_name)
        except ModuleNotFoundError as e:
            print('[E]', e)
            break

        module = getattr(imported, module_name)

        host = m_cfg.get('host', '0.0.0.0')
        port = int(m_cfg.get('port'))

        c = getattr(module, camel_cased(module_name))

        server = ThreadingTCPServer((host, port), c)
        servers.append(server)

        thread = Thread(target=server.serve_forever, daemon=True)
        threads.append(thread)

    for t in threads:
        t.start()

    while True:
        sleep(0.5)


if __name__ == "__main__":
    main()
