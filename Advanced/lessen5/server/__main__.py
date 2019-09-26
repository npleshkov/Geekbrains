import socket
import yaml
import json
from argparse import ArgumentParser
from datetime import datetime
from resolvers import find_server_action
from protocol import  vilidate_request, make_200, make_400,\
    make_404, make_500, config_request, config_rewrite

import logging

if __name__ == '__main__':

    config = config_request()
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=False,
                        help='Sets config path')
    parser.add_argument('-ht', '--host', type=str, required=False,
                        help='Sets config host')
    parser.add_argument('-p', '--port', type=str, required=False,
                        help='Sets config port')

    args = parser.parse_args()

    if args.config:
        with open(args.config) as file:
            file_config = yaml.safe_load(file)
            config.update(file_config or {})

    host = args.host if args.config else config.get('host')
    port = args.port if args.config else config.get('port')
    buffersize = config.get('buffersize')

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    formatter =logging.Formatter('%(asctime)s - %(levelname)s -%(message)s')

    file_handler = logging.FileHandler('server.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler())


try:
    sock = socket.socket()
    try:
        sock.bind((host, port))
    except OSError as e:
        if e.errno == 98:
            if port == 8008:
                port = 3000
                print(f'Текущий порт занят, выбран порт {port}')
            elif port == 3000:
                port = 8008
                print(f'Текущий порт занят, выбран порт {port}')
            else:
                print(f'Зарезервериванные порты 8008 и 3000 заняты. Остановите ранее запущенные серверы')
            config_rewrite(port)
            sock.bind((host, port))
    sock.listen(5)
    print(f'Server started with {host}:{port}')
    action_mapping = find_server_action()

    while True:
        client, (client_host, client_port) = sock.accept()
        logger.info(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize)
        request = json.loads(bytes_request)

        if vilidate_request(request):
            action = request.get('action')
            controller = action_mapping.get(action)
            if controller:
                try:
                    response = make_200(request, request.get('data'))
                    logger.debug(f'Request: {bytes_request.decode()}')
                except Exception as er:
                    response = make_500(request)
                    logger.critical(er)
            else:
                response = make_404(request, request.get('data'))
                logger.error(f'Wrong request: {request}')
        else:
            response = make_404(request, request.get('data'))
            logger.error(f'Wrong request: {request}')
        string_response = json.dumps(response)
        client.send(string_response.encode())
        client.close()
except KeyboardInterrupt:
    logger.info('Server shotdown')