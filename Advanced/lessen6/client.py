import sys
import yaml
import socket
import json
from argparse import ArgumentParser
from datetime import datetime

CONFIG_FILE = 'conf/config.yml'


def make_request(action, text, token_id, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'token': token_id,
        'time': date.timestamp()
    }


def config_request():
    with open(CONFIG_FILE) as file:
        config = yaml.safe_load(file)
    return config

def make_request_token():
    pass

if __name__ == '__main__':

    config = config_request()
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=False,
                        help='Sets config path')
    parser.add_argument('-ht', '--host', type=str, required=False,
                        help='Sets config host')
    parser.add_argument('-p', '--port', type=int, required=False,
                        help='Sets config port')

    args = parser.parse_args()

    if args.config:
        with open(args.config) as file:
            file_config = yaml.safe_load(file)
            config.update(file_config or {})

    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    sock = socket.socket()
    sock.connect((host, port))

    # login = input('Enter login: ')
    # password = input('Enter password: ')
    token_id = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U1'
    # request_token = make_request_token(token)



    action = input('Enter action name: ')
    message = input('Enter your message: ')
    request = make_request(action, message, token_id)
    string_request = json.dumps(request)

    sock.send(string_request.encode())
    bytes_response = sock.recv(buffersize)
    response = json.loads(bytes_response)
    print(response)
    print(f'Send message to {host}:{port}')
    sock.close()
