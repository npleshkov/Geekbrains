import sys
import yaml
import socket
import json
import zlib
from argparse import ArgumentParser
from datetime import datetime

CONFIG_FILE = 'conf/config.yml'
READ_MODE = 'r'
WRITE_MODE = 'w'

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
    parser.add_argument('-m', '--mode', type=str, default=READ_MODE,
                        help='Sets config mode')

    args = parser.parse_args()

    if args.config:
        with open(args.config) as file:
            file_config = yaml.safe_load(file)
            config.update(file_config or {})

    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    try:
        sock = socket.socket()
        sock.connect((host, port))
        while True:
            if args.mode == WRITE_MODE:
                # login = input('Enter login: ')
                # password = input('Enter password: ')
                action = input('Enter action name: ')
                message = input('Enter your message: ')

                token_id = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U'
                # request_token = make_request_token(token)


                request = make_request(action, message, token_id)
                string_request = json.dumps(request)
                bytes_request = string_request.encode()
                compessed_request = zlib.compress(bytes_request)
                sock.send(compessed_request)
            else:
                compressed_response = sock.recv(buffersize)
                bytes_responce = zlib.decompress(compressed_response)
                response = json.load(bytes_responce)
                print(compressed_response)
                print(response)
    except KeyboardInterrupt:
        print('Client shutdown')


    # response = json.loads(compessed_request)
    # bytes_response = sock.recv(buffersize)
    #
    # compress_response = sock.recv((buffersize))
    # bytes_response = zlib.decompress(compress_response)
    # response = json.load(bytes_response)
    #
    #
    # print(response)
    # print(f'Send message to {host}:{port}')
    # # sock.close()
