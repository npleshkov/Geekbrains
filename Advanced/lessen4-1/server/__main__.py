import socket
import yaml
import json
from argparse import ArgumentParser
from protocol import vilidate_request, make_200, make_400, make_404, make_500
from resolvers import  find_server_action

config_file = 'conf/config.yml'


def config_request():
    with open(config_file) as file:
        config = yaml.safe_load(file)
    return config


def config_rewrite(port):
    with open(config_file) as file_r:
        config = yaml.safe_load(file_r)
    with open(config_file, 'w') as file:
        config['port'] = port
        yaml.safe_dump(config, file)
    return config


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
        print(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize)
        request = json.loads(bytes_request)

        if vilidate_request(request):
            action = request.get('action')
            controller = action_mapping.get(action)
            if controller:
                try:
                    response = controller(request)
                    print(f'Request: {bytes_request.decode()}')
                except Exception as er:
                    response = make_500(request)
                    print(er)
            else:
                response = make_404(request)
        else:
            response = make_404(request, request.get('data'))
            print(f'Wrong request: {request}')
        string_response = json.dumps(response)
        client.send(string_response.encode())
        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
