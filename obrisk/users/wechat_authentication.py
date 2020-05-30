import logging
import hashlib
import random
import time
from urllib import parse
from xml.etree.ElementTree import fromstring
import requests

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import (
        login,authenticate,get_user_model
    )

from obrisk.users import wechat_config


Users = get_user_model()


class WechatOpenidAuth(object):
    def get_user(self, id_):
        try:
            return Users.objects.get(pk=id_)
        except Users.DoesNotExist:
            return None

    def authenticate(self, openid=None):
        try:
            user = Users.objects.get(openid=openid)
            if user is not None:
                return user

        except Users.DoesNotExist:
            return None

    def login(request, openid):
      try:
            user = authenticate(openid=openid)
            login(request, user)
            print("Huuray",auth)
      except Exception as e:
          logging.error(f'wechat user logging in failed: {e}')



# -*- coding: utf-8 -*-
# ----------------------------------------------
# @Time    : 18-3-21 下午1:36
# @Author  : YYJ
# @File    : WechatAPI.py
# @CopyRight: ZDWL
# ----------------------------------------------



class WechatAPI(object):
    def __init__(self):
        self.config = wechat_config
        self._access_token = None
        self._openid = None

    @staticmethod
    def process_response_login(rsp):
        """解析微信登录返回的json数据，返回相对应的dict, 错误信息"""
        if 200 != rsp.status_code:
            return None, {'code': rsp.status_code, 'msg': 'http error'}
        try:
            content = rsp.json()

        except Exception as e:
            return None, {'code': 9999, 'msg': e}
        if 'errcode' in content and content['errcode'] != 0:
            return None, {'code': content['errcode'], 'msg': content['errmsg']}

        return content, None

    @staticmethod
    def create_time_stamp():
        """产生时间戳"""
        now = time.time()
        return int(now)

    @staticmethod
    def create_nonce_str(length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    @staticmethod
    def xml_to_array(xml):
        """将xml转为array"""
        array_data = {}
        root = fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def array_to_xml(self, dic, sign_name=None):
        """array转xml"""
        if sign_name is not None:
            dic[sign_name] = self.get_sign()
        xml = ["<xml>"]
        for k in dic.keys():
            xml.append("<{0}>{1}</{0}>".format(k, dic[k]))
        xml.append("</xml>")
        return "".join(xml)


class WechatLogin(WechatAPI):
    def get_code_url(self):
        """微信内置浏览器获取网页授权code的url"""
        url = self.config.defaults.get('wechat_browser_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(self.config.REDIRECT_URI),
             self.config.SCOPE, self.config.STATE if self.config.STATE else ''))
        return url

    def get_code_url_pc(self):
        """pc浏览器获取网页授权code的url"""
        url = self.config.defaults.get('pc_QR_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(self.config.REDIRECT_URI), self.config.PC_LOGIN_SCOPE,
             self.config.STATE if self.config.STATE else ''))
        return url

    def get_access_token(self, code):
        """获取access_token"""
        params = {
            'appid': self.config.APPID,
            'secret': self.config.APPSECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        token, err = self.process_response_login(requests
                                                 .get(self.config.defaults.get('wechat_browser_access_token'),
                                                      params=params))
        if not err:
            self._access_token = token['access_token']
            self._openid = token['openid']
        return self._access_token, self._openid

    def get_user_info(self, access_token, openid):
        """获取用户信息"""
        params = {
            'access_token': access_token,
            'openid': openid,
            'lang': self.config.LANG
        }
        return self.process_response_login(requests
                                           .get(self.config.defaults.get('wechat_browser_user_info'), params=params))
