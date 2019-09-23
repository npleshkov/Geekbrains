import pytest
from datetime import datetime
from protocol import make_response, make_404, make_400, make_200, \
    make_500, config_request
from resolvers import find_server_action

CODE = 200
TIME = datetime.now().timestamp()
ACTION = 'echo'
DATA = 'some client data'
DATA_404 = f'Action "{ACTION}" not found'
DATA_505 = 'Internal server error'
CONFIG_FILE = 'conf/config.yml'
PORT = [8008, 3000]

REQUEST = {
    'action': ACTION,
    'time': TIME,
    'data': 'some client data'
}


# RESPONSE = {
#     'action': 'test',
#     'time': TIME,
#     'code': CODE,
#     'data': DATA
# }


# def test_make_responce():
#     response = make_response()
#     assert False

def test_action_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('action')
    assert action == ACTION


def test_code_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('code')
    assert action == CODE


def test_time_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('time')
    assert action == TIME


def test_data_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('data')
    assert action == DATA


def test_none_request_make_response():
    with pytest.raises(AttributeError):
        response = make_response(None, CODE)


def test_code_make_400():
    response = make_400(REQUEST, DATA, date=TIME)
    action = response.get('code')
    assert action == 400


def test_data_make_400():
    response = make_400(REQUEST, DATA, date=TIME)
    action = response.get('data')
    assert action == DATA


def test_time_make_400():
    response = make_400(REQUEST, DATA, date=TIME)
    action = response.get('time')
    assert action == TIME


def test_code_make_404():
    response = make_404(REQUEST, date=TIME)
    action = response.get('code')
    assert action == 404


def test_data_make_404():
    response = make_404(REQUEST, date=TIME)
    action = response.get('data')
    assert action == DATA_404


def test_time_make_404():
    response = make_404(REQUEST, date=TIME)
    action = response.get('time')
    assert action == TIME


def test_code_make_200():
    response = make_200(REQUEST, DATA, date=TIME)
    action = response.get('code')
    assert action == CODE


def test_data_make_200():
    response = make_200(REQUEST, DATA, date=TIME)
    action = response.get('data')
    assert action == DATA


def test_time_make_200():
    response = make_200(REQUEST, DATA, date=TIME)
    action = response.get('time')
    assert action == TIME


def test_code_make_500():
    response = make_500(REQUEST, date=TIME)
    action = response.get('code')
    assert action == 500


def test_data_make_500():
    response = make_500(REQUEST, date=TIME)
    action = response.get('data')
    assert action == DATA_505


def test_port_config_request():
    response = config_request()
    if response.get('port') not in PORT:
        assert False


def test_find_controllers():
    action_mapping = find_server_action()
    controllers = action_mapping.get(ACTION)
    controller = controllers(REQUEST).get('action')
    assert ACTION == controller
