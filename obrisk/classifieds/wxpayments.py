import logging
import hashlib
import xmltodict
import time
import requests
import random
import string
from random import Random

from ipware import get_client_ip
from bs4 import BeautifulSoup
from django.core.cache import cache
from config.settings.base import env


APPID = env('WECHAT_APPID')
APP_SECRET = env('WECHAT_APPSECRET')
API_KEY = env('WECHAT_API_KEY')
# On wechat merchant ac, account settings then security API
MCH_ID = env.int('WECHAT_MERCHANT_ID')
MCHID = MCH_ID + 1 - 1
WXORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
NOTIFY_URL = "https://obrisk.com/classifieds/wsguatpotlfwccdi/wxjsapipy/inwxpy_results"


def get_md5(data, salt=True):
    if salt:
        return hashlib.md5('get{0}{1}md5'.format(data, time.time()).encode(encoding='UTF-8')).hexdigest()
    else:
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def get_sign_str(sign_dict):
    data = ''
    sort_keys = sorted(sign_dict)  # 从小到大排序
    for i, key in enumerate(sort_keys):
        data += '{0}={1}&'.format(key, sign_dict.get(key, ''))
    data += 'key={0}'.format(API_KEY)

    sign = get_md5(data, False).upper()
    logging.error('%s', data, stack_info=True, extra={'sign': sign})
    return sign


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

    logging.error('%s', params_str, stack_info=True, extra={'sign': sign})
    return sign


def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


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


def get_xml_str(sign_dict):
    xml_data = '<xml>'
    for k, v in sign_dict.items():
        xml_data += '<{0}>{1}</{0}>'.format(k, v)
    xml_data += '</xml>'

    return xml_data


def wx_pay_unifiedorder(detail):
    """
    Visit WarmPay unified ordering interface
    :param detail:
    :return:
    """
    xml = get_xml_str(detail)
    logging.error(xml)

    #detail['sign'] = get_sign(detail, API_KEY)
    #xml = trans_dict_to_xml(data)  # 转换字典为XML
    # 以POST方式向微信公众平台服务器发起请求
    response = requests.request('post', WXORDER_URL, data=xml)
    # 将请求返回的数据转为字典
    #data_dict = trans_xml_to_dict(response.content)
    return response.content


def create_out_trade_no():
        """
        创建微信商户订单号
        :return:
        """
        local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        result = 'wx{}'.format(local_time[2:])
        return result


def get_jsapi_params(request, openid, title, details, total_fee):
    """
    Get the parameters required for WeChat Jsapi payment
    :param openid: 用户的openid
    :return:
    """
    client_ip = cache.get(
            f'user_ipaddr_{openid}'
        )
    if client_ip is None:
        client_ip, _ = get_client_ip(
                request,
                proxy_trusted_ips=['63.0.0.5','63.1']
            )

        cache.set(
                f'user_ipaddr_{openid}',
                client_ip,
                60 * 60 * 2
            )
    params = {
        'appid': APPID,  # APPID
        'attach':'{0}'.format(title),  # 商品描述
        'body': '{0}'.format(details),  # 商品描述
        'mch_id': MCHID,  # 商户号
        'nonce_str': random_str(16),  # 随机字符串
        'notify_url': NOTIFY_URL,  # 微信支付结果回调url
        'openid': openid,
        'out_trade_no': create_out_trade_no(),  # 订单号
        'spbill_create_ip': client_ip,  # 发送请求服务器的IP地址
        'total_fee': int(round(float(total_fee), 2) * 100),  # 订单总金额,1代表1分钱
        'trade_type': 'JSAPI'
    }
    # 调用微信统一下单支付接口url

    params['sign'] = get_sign(params, API_KEY)
    notify_result = wx_pay_unifiedorder(params)
    notify_result = trans_xml_to_dict(notify_result)
    # print('向微信请求', notify_result)
    if 'return_code' in notify_result and notify_result['return_code'] == 'FAIL':
        return {'error': notify_result['return_msg']}
    if 'prepay_id' not in notify_result:
        return {'error': 'Prepay_id not returned successfully'}
    params['prepay_id'] = notify_result['prepay_id']
    params['timeStamp'] = int(time.time())
    params['nonceStr'] = random_str(16)
    params['sign'] = get_sign({'appId': APPID,
                       "timeStamp": params['timeStamp'],
                       'nonceStr': params['nonceStr'],
                       'package': 'prepay_id=' + params['prepay_id'],
                       'signType': 'MD5',
                   },
                   API_KEY
               )
    ret_params = {
        'package': "prepay_id=" + params['prepay_id'],
        'appid': APPID,
        'timeStamp': str(params['timeStamp']),
        'nonceStr': params['nonceStr'],
        'sign': params['sign'],

    }
    return ret_params


# 统一下单
# 生成nonce_str
def generate_randomStr():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


# 生成签名
def generate_sign(param):
    stringA = ''
    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += k + "=" + str(param[k]) + "&"
    # 拼接商户KEY
    stringSignTemp = stringA + "key=" + API_KEY
    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()
    return sign


# 发送xml请求
def send_xml_request(url, param):
    # dict 2 xml
    param = {'root': param}
    xml = xmltodict.unparse(param)

    response = requests.post(
            url, data=xml.encode('utf-8'),
            headers={'Content-Type': 'text/xml'}
        )
    # xml 2 dict
    #msg = response.text
    #xmlmsg = xmltodict.parse(msg)
    response.encoding = 'utf-8'
    #return trans_xml_to_dict(response.text)
    return xmltodict.parse(response.text)


# 统一下单
def iget_jsapi_params(openid, details, fee):
    url = WXORDER_URL
    nonce_str = generate_randomStr()        # 订单中加nonce_str字段记录（回调判断使用）
    out_trade_no = order_num('1202')     # 支付单号，只能使用一次，不可重复支付
    '''
    order.out_trade_no = out_trade_no
    order.nonce_str = nonce_str
    order.save()
    '''

    # 1. 参数
    param = {
        "appid": APPID,
        "mch_id": MCHID,    # 商户号
        "nonce_str": nonce_str,     # 随机字符串
        "body": details,     # 支付说明
        "out_trade_no": out_trade_no,   # 自己生成的订单号
        "total_fee": fee,
        #"spbill_create_ip": CREATE_IP,    # 发起统一下单的ip "notify_url": NOTIFY_URL,
        "trade_type": 'JSAPI',      # 小程序写JSAPI
        "openid": openid,
    }
    # 2. 统一下单签名
    sign = generate_sign(param)
    param["sign"] = sign  # 加入签名
    # 3. 调用接口

    xmlmsg = send_xml_request(url, param)
    # 4. 获取prepay_id
    if xmlmsg['xml']['return_code'] == 'SUCCESS':
        if xmlmsg['xml']['result_code'] == 'SUCCESS':
            prepay_id = xmlmsg['xml']['prepay_id']
            # 时间戳
            timeStamp = str(int(time.time()))
            # 5. 根据文档，六个参数，否则app提示签名验证失败，https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12
            data = {
                "appid": APPID,
                "partnerid": MCHID,
                "prepayid": prepay_id,
                "package": "Sign=WXPay",
                "noncestr": nonce_str,
                "timestamp": timeStamp,
            }            # 6. paySign签名
            paySign = generate_sign(data)
            data["paySign"] = paySign  # 加入签名
            # 7. 传给前端的签名后的参数
            return data
    return {'error': xmlmsg['xml']['return_msg'] }
