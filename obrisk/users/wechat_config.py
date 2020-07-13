# -*- coding: utf-8 -*-
# ----------------------------------------------
from config.settings.base import env
# ----------------------------------------------微信公众号---------------------------------------------- #
# 公众号appid
APPID = env('WECHAT_APPID')
# 公众号AppSecret
APPSECRET = env('WECHAT_APPSECRET')

# ----------------------------------------------微信商户平台---------------------------------------------- #
# 商户id
API_KEY = env('SECRET_KEY')

# ----------------------------------------------回调页面---------------------------------------------- #
# 用户授权获取code后的回调页面，如果需要实现验证登录就必须填写
REDIRECT_URI = 'https://in.obrisk.com/wx-auth'
PC_LOGIN_REDIRECT_URI = 'https://d.obrisk.com/wx-auth'

defaults = {
    # 微信内置浏览器获取code微信接口
    'wechat_browser_code': 'https://open.weixin.qq.com/connect/oauth2/authorize',
    # 微信内置浏览器获取access_token微信接口
    'wechat_browser_access_token': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 微信内置浏览器获取用户信息微信接口
    'wechat_browser_user_info': 'https://api.weixin.qq.com/sns/userinfo',
    # pc获取登录二维码接口
    'pc_QR_code': 'https://open.weixin.qq.com/connect/qrconnect',
    # pc获取登录二维码接口
    # 'pc_QR_code': 'https://api.weixin.qq.com/sns/userinfo',
}

#SCOPE = snsapi_userinfo or snsapi_base
SCOPE = 'snsapi_userinfo'
PC_LOGIN_SCOPE = 'snsapi_login'
STATE = ''
LANG = 'en_US'

CHINA_PROVINCES = ['Anhui', 'Beijing', 'Chongqing','Fujian', 'Gansu', 'Guangdong', 'Guizhou',
        'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei',
        'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai',
        'Shanghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Taiwan', 'Tianjin', 'Yunnan', 'Zhejiang']
