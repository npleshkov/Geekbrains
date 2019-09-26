import pytest

from datetime import datetime

from protocol import make_response, config_request

from resolvers import find_server_action


@pytest.fixture
def expected_code():
    return 200


@pytest.fixture
def expected_action():
    return 'echo'


@pytest.fixture
def expected_time():
    return datetime.now().timestamp()


@pytest.fixture
def expected_data():
    return 'some client data'


@pytest.fixture
def initial_request(expected_action, expected_time,
                    expected_data):
    return {
        'action': expected_action,
        'time': expected_time,
        'data': expected_data
    }


DATA_404 = f'Action "{expected_action}" not found'
DATA_505 = 'Internal server error'
CONFIG_FILE = 'conf/config.yml'
PORT = [8008, 3000]


# REQUEST = {
#     'action': ACTION,
#     'time': TIME,
#     'data': 'some client data'
# }

# RESPONSE = {
#     'action': 'test',
#     'time': TIME,
#     'code': CODE,
#     'data': DATA
# }


# def test_make_responce():
#     response = make_response()
#     assert False

def test_action_make_response(initial_request, expected_action, expected_code,
                              expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data,
                             date=expected_time)
    assert response.get('action') == expected_action


def test_code_make_response(initial_request, expected_code, expected_data,
                            expected_time):
    response = make_response(initial_request, expected_code, expected_data,
                             date=expected_time)
    assert response.get('code') == expected_code


def test_time_make_response(initial_request, expected_code, expected_data,
                            expected_time):
    response = make_response(initial_request, expected_code, expected_data,
                             date=expected_time)
    assert response.get('time') == expected_time


def test_data_make_response(initial_request, expected_code, expected_data,
                            expected_time):
    response = make_response(initial_request, expected_code, expected_data,
                             date=expected_time)
    assert response.get('data') == expected_data


def test_none_request_make_response(expected_code):
    with pytest.raises(AttributeError):
        response = make_response(None, expected_code)


def test_port_config_request():
    response = config_request()
    if response.get('port') not in PORT:
        assert False

def test_find_controllers(initial_request, expected_action):
    action_mapping = find_server_action()
    controllers = action_mapping.get(expected_action)
    controller = controllers(initial_request).get('action')
    assert expected_action == controller
