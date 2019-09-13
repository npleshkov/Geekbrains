import sys
import yaml
import socket
import json

from argparse import ArgumentParser

# SERVER_ADDRESS = 'localhost:8000'

def make_request(text):
    return {
        'data': text
    }

if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 8008,
        'buffersize': 1024
    }

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

    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    sock = socket.socket()
    sock.connect((host, port))

    # print(sys.argv)
    # server_address = input('Enter server address: ')
    message = input('Enter your message: ')
    request = make_request(message)
    print(request)
    string_request = json.dumps(request)

    sock.send(string_request.encode())
    bytes_response = sock.recv(buffersize)
    response = json.loads(bytes_response)
    print(response)
    print(f'Send message to {host}:{port}')
    #
    sock.close()
