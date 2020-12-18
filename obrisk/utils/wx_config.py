import time
import random
import string
import hashlib
import requests

from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from config.settings.base import env
from obrisk.utils.helpers import ajax_required

class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonce_str': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15)) #noqa

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)]) #noqa
        print (string)
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret


def get_fresh_token():
    APPID = env('WECHAT_APPID')
    APPSECRET = env('WECHAT_APPSECRET')

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}' #noqa

    failure_resp = JsonResponse({
        'success': False
    })

    try:
        token = requests.get(url, timeout=30)
        ACCESS_TOKEN = token.access_token

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to request wx credentials" + e)
        return failure_resp

    try:
        ticket_url = f'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={ACCESS_TOKEN}&type=jsapi' #noqa
        ticket = requests.get(ticket_url, timeout=30)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to request wx ticket" + e)
        return failure_resp

    cache.set('wx_jsapi_ticket', ticket.ticket, ticket.expires_in)


@ajax_required
@require_http_methods(["GET"])
def request_wx_credentials(request):

    try:
        ticket = cache.get('wx_jsapi_ticket')
    except:
        get_fresh_token()
    else:
        sign = Sign(ticket, request.build_absolute_uri)
        return JsonResponse ({
            'success': True,
            'info': sign.sign()
        })
