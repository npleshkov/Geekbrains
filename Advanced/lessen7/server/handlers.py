import logging
import json

from protocol import validate_request, make_200, make_404, make_500
from middlewares import compression_middleware


@compression_middleware
def handle_tcp_request(byte_request, action_mapping):
    request = json.load(byte_request)
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

    strinrg_response = json.dump(response)
    return strinrg_response

