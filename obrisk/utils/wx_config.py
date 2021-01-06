import time
import random
import string
import hashlib
import requests
import json
import logging

from json import JSONEncoder
from django.core.cache import cache
from django.http import (
        HttpResponse, JsonResponse
    )
from django.views.decorators.http import require_http_methods
from config.settings.base import env
from obrisk.utils.helpers import ajax_required


APPID = env('WECHAT_APPID')
APPSECRET = env('WECHAT_APPSECRET')


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
        unsinged_str = '&'.join(['{}={}'.format(key.lower(), self.ret[key]) for key in sorted(self.ret)]) #noqa
        self.ret['signature'] = hashlib.sha1(unsinged_str.encode("utf-8")).hexdigest()
        self.ret['success'] = True

        print(self.ret['signature'])
        return self.ret


def get_fresh_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}' #noqa

    try:
        token = requests.get(url, timeout=30)
        if token.ok:
            tkn = json.loads(token.text)
            ACCESS_TOKEN = tkn['access_token']
        else:
            return False

    except (AttributeError,
            KeyError,
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to request wx credentials" + e)
        return False

    try:
        ticket_url = f'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={ACCESS_TOKEN}&type=jsapi' #noqa
        ticket = requests.get(ticket_url, timeout=30)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to request wx ticket" + e)
        return False

    if ticket.ok:
        tkt = json.loads(ticket.text)
        if tkt['ticket'] is not None:
            cache.set(
                    'wx_jsapi_ticket',
                    tkt['ticket'],
                    tkt['expires_in']
                )
            return True
    return False


class SignEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

@ajax_required
@require_http_methods(["GET"])
def request_wx_credentials(request):
    '''This view returns the credentials used to initialize
    wechat JavaScript object'''
    ticket = None

    try:
        ticket = cache.get('wx_jsapi_ticket')
        if ticket is None:
            get_fresh_token()
    except:
        if get_fresh_token():
            ticket = cache.get('wx_jsapi_ticket')
        else:
            return JsonResponse({'success': False})

    finally:
        sign = Sign(ticket, request.META['HTTP_REFERER'])
        SignEncoder().encode(sign)
        res = sign.sign()
        return JsonResponse(json.dumps(res, cls=SignEncoder), safe=False)
