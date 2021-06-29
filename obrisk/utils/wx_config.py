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
            'noncestr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15)) #noqa

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        unsinged_str = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)]) #noqa
        self.ret['signature'] = hashlib.sha1(unsinged_str.encode('utf-8')).hexdigest()
        self.ret['success'] = True
        self.ret['id'] = APPID

        return self.ret


def get_access_token():

    wxtkn = cache.get('wx_access_tkn')
    if wxtkn is not None:
        return wxtkn

    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}' #noqa
    try:
        token = requests.get(url, timeout=30)
        if token.ok:
            tkn = json.loads(token.text)
            cache.set(
                    'wx_access_tkn',
                    tkn['access_token'],
                    tkn['expires_in'] - 300
                )
            return tkn['access_token']
        else:
            return None

    except KeyError as e:
        try:
            tkn = json.loads(token.text)
            if tkn['errcode'] == -1:
                time.sleep(1)
                return get_access_token()

        except Exception as e:
            logging.error(
                    f"Failed to get Wechat access token and errcode is not -1 {e}"
                )
            return None

    except (AttributeError,
            TypeError,
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error(f"Failed to request access token from Wechat {e}")
        return None


def get_fresh_token():
    ACCESS_TOKEN = get_access_token()
    if ACCESS_TOKEN is None:
        return False

    try:
        ticket_url = f'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={ACCESS_TOKEN}&type=jsapi' #noqa
        ticket = requests.get(ticket_url, timeout=30)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error(f"Failed to request wx ticket: {e}")
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


def get_user_info(token, user_id, lang='en_US'):
    try:
        response = requests.get(
            url="https://api.weixin.qq.com/cgi-bin/user/info",
            params={
                "access_token": token,
                "openid": user_id,
                "lang": lang
            }
        )
        response.encoding = 'utf8'
        if response.ok:
            return response.json()

    except (AttributeError,
            TypeError,
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error(f"Failed to request access token from Wechat {e}")
    return None


class SignEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@ajax_required
@require_http_methods(["GET"])
def request_wx_credentials(request):
    '''This view returns the credentials used to initialize
    wechat JavaScript object'''

    ticket = cache.get('wx_jsapi_ticket')
    if ticket is None:
        if get_fresh_token():
            ticket = cache.get('wx_jsapi_ticket')
        else:
            return JsonResponse({'success': False})

    sign = Sign(ticket, request.META['HTTP_REFERER'])
    SignEncoder().encode(sign)
    res = sign.sign()
    return JsonResponse(json.dumps(res, cls=SignEncoder), safe=False)
