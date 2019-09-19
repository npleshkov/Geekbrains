from functools import reduce

from settings import INSTALLED_APPS

def find_server_action():
    application = reduce(
        lambda value, item: value + [__import__(f'{item}.routes')],
        INSTALLED_APPS, []
    )
    routes = reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        application, []
    )
    mapping = reduce(
        lambda value, item: value + getattr(item, 'actionmapping', []),
        routes, []
    )
    return {item.get('action'):item.get('controller') for item in mapping if item}

def resolv(action, routes):
    return routes.get(action)