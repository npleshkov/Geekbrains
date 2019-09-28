import socket
import yaml
import json
import logging
import jwt
import select
from argparse import ArgumentParser
from handlers import handle_tcp_request

from resolvers import find_server_action

from protocol import config_request, config_rewrite

config = config_request()

# header = { "alg": "HS256", "typ": "JWT"}
# payload = {'userId': 'b08f86af-35da-48f2-8fab-cef3904660bd'}
# encoded = jwt.encode(payload, 'secret', algorithm='HS256')
# # print(encoded)

# print(jwt.decode(encoded, 'secret', algorithms=['HS256']))
parser = ArgumentParser()

parser.add_argument('-c', '--config', type=str, required=False,
                    help='Sets config path')
parser.add_argument('-ht', '--host', type=str, required=False,
                    help='Sets config host')
parser.add_argument('-p', '--port', type=str, required=False,
                    help='Sets config port')
# # parser.add_argument('-m', '--mode', type=str, required=False,
#                     help='Sets config port')

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

requests = []
connections = []

try:
    sock = socket.socket()
    try:
        sock.bind((host, port))
        # sock.setblocking(False)
        # sock.settimeout(1)
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
    sock.setblocking(0)
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()

    while True:
        try:
            client, (client_host, client_port) = sock.accept()
            logging.info(f'Client {client_host}:{client_port} was connected')
            connections.append(client)
        except:
            # continue
            pass

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )
        for read_client in rlist:
            bytes_request = read_client.recv(buffersize)
            requests.append(bytes_request)
        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_tcp_request(bytes_request, action_mapping)
            print(f'bytes_response {bytes_response}')
            for write_client in wlist:
                write_client.send(bytes_response)

          # try:
          #       jwt.decode(bytes_response.get('token'), 'secret',
          #                  algorithms=['HS256'])
          #       for write_client in wlist:
          #           write_client.send(bytes_response)
          #           print('send')
          #   except jwt.exceptions.InvalidSignatureError:
          #       pass
          #       logging.error(
          #       f'Wrong token: {bytes_response.get("token")} not found')
          #       string_response = json.dumps('token error')
          #       read_client.send(string_response.encode())

        # # read_client.send(bytes_response)
        # # client.close()
except KeyboardInterrupt:
    logging.info('Server shotdown')
