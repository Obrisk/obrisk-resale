from django.utils.crypto import get_random_string
import string

VALID_KEY_CHARS = string.ascii_lowercase + string.digits

def visitorid_middleware(get_response):
    def middleware(request):
        if not request.session.get('visitor_id'):
            request.session['visitor_id'] = get_random_string(32, VALID_KEY_CHARS)
        response = get_response(request)
        return response
    return middleware
