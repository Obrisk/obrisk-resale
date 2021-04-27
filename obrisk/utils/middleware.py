import string
from django.utils.crypto import get_random_string
from ipware import get_client_ip

VALID_KEY_CHARS = string.ascii_lowercase + string.digits

def visitorid_middleware(get_response):
    def middleware(request):
        if request.session.get('visitor_id') is None:
            client_ip, _ = get_client_ip(
                    request
                )
            request.session['visitor_id'] = client_ip + get_random_string(32, VALID_KEY_CHARS)
            #This code assumes get_random_string generate unique strings
            #Which is not true. There has to be a way to query all existing sessions values
        response = get_response(request)
        return response
    return middleware
