from datetime import datetime

def timestap_controller(request):
    return make_200(request, datetime.now().timestamp())