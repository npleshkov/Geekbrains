from protocol import make_response
from  datetime import  datetime

CODE = 200
DATE = datetime.now().timestamp()
REQUEST = {
    'action': 'test',
    'time': DATE,
    'data': 'some client data'
}
RESPONSE = {
    'action': 'test',
    'time': DATE,
    'code': CODE,
    'data': ''
}

# def test_make_responce():
#     response = make_response()
#     assert True

def test_make_responce():
    response = make_response()
    assert response = RESPONSE

