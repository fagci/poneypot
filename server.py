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

    servers = []
    threads = []

    for module_name in cfg_parser.sections():
        cfg = cfg_parser[module_name]

        if not cfg.get('enabled'):
            continue

        try:
            imported = __import__('modules.%s' % module_name)
        except ModuleNotFoundError as e:
            print('[E]', e)
            return

        module = getattr(imported, module_name)

        host = cfg.get('host', '0.0.0.0')

        c = getattr(module, camel_cased(module_name))

        for port in cfg.get('port').split(','):
            p = int(port.strip())
            print('[*] Run', module_name, 'on', p)
            server = ThreadingTCPServer((host, p), c)
            servers.append(server)

            thread = Thread(target=server.serve_forever, daemon=True)
            threads.append(thread)

    for t in threads:
        t.start()

    while True:
        sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by user')
        exit(130)
