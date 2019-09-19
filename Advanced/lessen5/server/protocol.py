import yaml
from datetime import datetime

CONFIG_FILE = 'conf/config.yml'


def config_request():
    with open(CONFIG_FILE) as file:
        config = yaml.safe_load(file)
    return config

def config_rewrite(port):
    with open(CONFIG_FILE) as file_r:
        config = yaml.safe_load(file_r)
    with open(CONFIG_FILE, 'w') as file:
        config['port'] = port
        yaml.safe_dump(config, file)
    return config


def vilidate_request(request):
    return 'action' in request and 'time' in request and request.get('action') and request.get(
        'time')


def make_response(request, code, data=None, date=datetime.now()):
    return {
        'action': request.get('action'),
        'time': date.timestamp() if isinstance(date, datetime) else date,
        'code': code,
        'data': data
    }


def make_400(request, data=None, date=datetime.now()):
    return make_response(request, 400, data, date)


def make_404(request, date=datetime.now()):
    return make_response(request, 404, f'Action "{request.get("action")}" not found', date)


def make_200(request, data=None, date=datetime.now()):
    return make_response(request, 200, data, date)


def make_500(request, date=datetime.now()):
    return make_response(request, 500, 'Internal server error', date)
