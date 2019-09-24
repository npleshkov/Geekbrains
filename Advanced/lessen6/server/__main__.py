import socket
import yaml
import json
import logging
import jwt
from argparse import ArgumentParser

from resolvers import find_server_action
from protocol import validate_request, make_404, make_500, \
    config_request, config_rewrite

config = config_request()
parser = ArgumentParser()

# header = { "alg": "HS256", "typ": "JWT"}
# payload = {'userId': 'b08f86af-35da-48f2-8fab-cef3904660bd'}
# encoded = jwt.encode(payload, 'secret', algorithm='HS256')
# # print(encoded)

# print(jwt.decode(encoded, 'secret', algorithms=['HS256']))

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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)

try:
    sock = socket.socket()
    try:
        sock.bind((host, port))
    except OSError as e:
        print(e.errno)
        if e.errno == 98:
            if port == 8008:
                port = 3000
                logging.debug(f'Текущий порт занят, выбран порт {port}')
            elif port == 3000:
                port = 8008
                logging.debug(f'Текущий порт занят, выбран порт {port}')
            else:
                logging.error(f'Зарезервериванные порты 8008 и 3000 заняты.\
                        Остановите ранее запущенные серверы')
            config_rewrite(port)
            sock.bind((host, port))
    sock.listen(5)
    logging.info(f'Server started with {host}:{port}')
    action_mapping = find_server_action()

    while True:
        client, (client_host, client_port) = sock.accept()
        logging.info(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize)
        request = json.loads(bytes_request)

        try:
            jwt.decode(request.get('token'), 'secret', algorithms=['HS256'])
            if validate_request(request):
                action = request.get('action')
                controller = action_mapping.get(action)
                if controller:
                    try:
                        response = controller(request)
                        logging.debug(f'Request: {bytes_request.decode()}')
                    except Exception as er:
                        response = make_500(request)
                        logging.critical(er)
                else:
                    response = make_404(request)
                    logging.error(f'Wrong request: {request} not found')
            else:
                response = make_404(request, 'Request is not valid')
                logging.error(f'Wrong request: {request} not found')
            string_response = json.dumps(response)
            client.send(string_response.encode())

        except jwt.exceptions.InvalidSignatureError:
            logging.error(f'Wrong token: {request.get("token")} not found')
            string_response = json.dumps('token error')
            client.send(string_response.encode())

        client.close()
except KeyboardInterrupt:
    logging.info('Server shotdown')
