import logging
import hashlib
import time
import requests
from collections import OrderedDict
from random import Random

from django.conf import settings
from bs4 import BeautifulSoup
from config.settings.base import env


APP_ID = env('WECHAT_APPID')
APP_SECRET = env('WECHAT_APPSECRET')
API_KEY = env('WECHAT_API_KEY')
# On wechat merchant ac, account settings then security API
MCH_ID = env('WECHAT_MERCHANT_ID')
WXORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
NOTIFY_URL = "https://obrisk.com/classifieds/wsguatpotlfwccdi/wxjsapipy/inwxpy_results"
CREATE_IP = getattr(settings, 'AWS_LOCAL_IP', '127.0.0.1')


def random_str(randomlength=8):
    """
    Generate random string
    :param randomlength: string length
    :return sting:
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def order_num(seed):
    """
    Generate the payment order,
    :param phone:
    :return:
    """
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    result = seed + 'T' + local_time + random_str(5)
    return result


def get_sign(data_dict, key):
    """
    Signature function, the parameters are the signed data and key
    """
    params_list = sorted(
        data_dict.items(), key=lambda e: e[0], reverse=False
    )  # 参数字典倒排序为列表
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # Organize the parameter string and add the merchant transaction key at the end
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign


def trans_dict_to_xml(data_dict):
    """
    Define the function of dictionary to XML
    """
    data_xml = []
    for k in sorted(data_dict.keys()):
        # 遍历字典排序后的key
        # 取出字典中key对应的value
        v = data_dict.get(k)

        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
            data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    # 返回XML，并转成utf-8，解决中文的问题
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')


def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


def wx_pay_unifiedorder(detail):
    """
    Visit WarmPay unified ordering interface
    :param detail:
    :return:
    """
    detail['sign'] = get_sign(detail, API_KEY)
    # print(detail)
    xml = trans_dict_to_xml(detail)  # 转换字典为XML
    # 以POST方式向微信公众平台服务器发起请求
    response = requests.request('post', WXORDER_URL, data=xml)
    # 将请求返回的数据转为字典
    # data_dict = trans_xml_to_dict(response.content)
    return response.content


def get_redirect_url():
    """
    Get the redirected url returned by WeChat
    :return: url,其中携带code
    """
    WeChatcode = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    urlinfo = OrderedDict()
    urlinfo['appid'] = APP_ID
    # Set redirect routing
    urlinfo['redirect_uri'] = 'https://obrisk.com/classifieds/wsguatpotlfwccdi/wxjsapipy/?getInfo=yes' #noqa
    urlinfo['response_type'] = 'code'
    urlinfo['scope'] = 'snsapi_base'  # 只获取基本信息
    urlinfo['state'] = 'mywxpay'   # 自定义的状态码
    info = requests.get(url=WeChatcode, params=urlinfo)
    return info.url


def get_openid(code,state):
    """
    Get openid of user
    :param code:
    :param state:
    :return:
    """
    if code and state and state == 'mywxpay':
        WeChatcode = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        urlinfo = OrderedDict()
        urlinfo['appid'] = APP_ID
        urlinfo['secret'] = APP_SECRET
        urlinfo['code'] = code
        urlinfo['grant_type'] = 'authorization_code'
        info = requests.get(url=WeChatcode, params=urlinfo)
        info_dict = eval(info.content.decode('utf-8'))
        return info_dict['openid']

    return None


def get_jsapi_params(openid, details, total_fee):
    """
    Get the parameters required for WeChat Jsapi payment
    :param openid: 用户的openid
    :return:
    """

    params = {
        'appid': APP_ID,  # APPID
        'mch_id': MCH_ID,  # 商户号
        'nonce_str': random_str(16),  # 随机字符串
        'out_trade_no': order_num('1202'),  # 订单编号,可自定义
        'total_fee': total_fee,  # 订单总金额
        'spbill_create_ip': CREATE_IP,  # 发送请求服务器的IP地址
        'openid': openid,
        'notify_url': NOTIFY_URL,  # 支付成功后微信回调路由
        'body': details,  # 商品描述
        'trade_type': 'JSAPI',  # 公众号支付类型
    }
    # print(params)
    # 调用微信统一下单支付接口url
    try:
        notify_result = wx_pay_unifiedorder(params)
        prepay_id = trans_xml_to_dict(notify_result)['prepay_id']
        params['timeStamp'] = int(time.time())
        params['nonceStr'] = random_str(16)
        params['package']: 'prepay_id=' + prepay_id
        params['sign'] = get_sign(
            {
                'appId': APP_ID,
                "timeStamp": params['timeStamp'],
                'nonceStr': params['nonceStr'],
                'package': 'prepay_id=' + prepay_id,
                'signType': 'MD5',
            },
            API_KEY
        )
    except Exception as e:
        logging.error(f'Cannot initiate wechat pay parameters: {e}')

    return params
