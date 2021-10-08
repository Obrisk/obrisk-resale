#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import logging
import requests
from urllib.request import urlopen
from django.utils import timezone
from django.db.models import Count

from obrisk.utils.wx_config import get_access_token
from obrisk.classifieds.models import Classified


request_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" #noqa


class WechatPush():
    def post_data(self,url,para_dct):
        """触发post请求微信发送最终的模板消息"""
        para_data = para_dct
        f = urlopen(url,para_data)
        content = f.read()
        return content

    def do_push(self,touser,template_id,url,topcolor,data):
        '''推送消息 '''
        token = get_access_token()
        if token is None:
            return None

        # 背景色设置,貌似不生效   
        if topcolor.strip() == '':
            topcolor = "#1faece"
        #最红post的求情数据
        dict_arr = {
                'touser': touser,
                'template_id':template_id,
                'url':url,
                'topcolor':topcolor,
                'data':data
            }

        logging.error(
            f'Pushing wechat notifications, dict arr',
            extra=dict_arr
        )

        json_template = json.dumps(dict_arr)
        #transfer to requests.

        #url, data=xml.encode('utf-8'),
        response = requests.post(
                request_url + token,
                data=json_template,
                headers={'Content-Type': 'application/json'}
            )
        #response.encoding = 'utf8'
        #msg = response.text
        #xmlmsg = xmltodict.parse(msg)
        #return trans_xml_to_dict(response.text)
        #读取json数据

        #j = json.loads(content)
        j = response.json()
        logging.error(
            f'Failed to notify seller on Classified Order',
            extra=j
        )
        j.keys()

        #if j['errcode'] != 0:
        logging.error(
                'Pushing Wx Template failed',
                extra=j
            )


def unread_msgs_wxtemplate(userid, last_msg, sender, time):
    wx_push = WechatPush()
    template_id = "TiTwvX3G9CshOdDUC0_-6XsEuTEhNMvqXaeeyznEvos"
    url = "https://obrisk.com/ws/messages/?dd=" + userid

    color = "#173177"
    title = "Hi you have received new messages, Click this link to view"
    tail = "Thank you for using Obrisk"

    data={
            "first": {"value":title},
            "keyword1":{
                "value":last_msg,"color":color
            },
            "keyword2":{
                "value":sender,"color":color
            },
            "keyword3":{
                "value":time,"color":color
            },
            "remark": {"value":tail}
        }

    wx_push.do_push(userid,template_id,url,color,data)


def upload_success_wxtemplate(user):
    wx_push = WechatPush()
    template_id = "fKuBPeGyH5rSF3wd_ECrM_dg2IiC-tDaGVJN_HKnrFo"

    #Get items uploaded 10 minutes ago by this user
    classifieds = Classified.objects.filter(
        user=user, status="A",
        timestamp__gt=timezone.now() - timezone.timedelta(minutes=30)
    )
    logging.error(f'Found classifieds: {classifieds}')

    if classifieds.count() > 1:
        url = f"https://obrisk.com/users/i/{user.username}/"
        title = f'Uploaded {classifieds.count()} items'
    elif classifieds.count() == 1:
        url = "https://obrisk.com/classifieds/{classifieds.first().slug}/"
        title = classifieds.first().title
    else:
        return None

    color = "#173177"
    title = f"Hi {user.username}, all eyes on your stuff selling🤗"
    tail = "Thank you for using Obrisk"

    data={
            "first": {"value":title},
            "keyword1":{
                "value":title,"color":color
            },
            "keyword2":{
                "value":'Few minutes ago', "color":color
            },
            "keyword3":{
                "value":user.city, "color":color
            },
            "keyword4":{
                "value":'Active', "color":color
            },
            "remark": {"value":tail}
        }

    logging.error(f'Pushing data: {data}', extra=data)
    wx_push.do_push(user.wechat_openid,template_id,url,color,data)


def notify_seller_wxtemplate(order):
    wx_push = WechatPush()
    template_id = "2DWnQShB7yDden_QxWevK_2F8f7RpexrI_WCXuvwDXo" #noqa
    url = "https://obrisk.com/classifieds/orders/wsguatpotlfwccdi/seller-confirm?or=" + order.slug #noqa

    color = "#173177"
    title = "Hi your item has been purchased😊"
    tail = "Thank you for using Obrisk"

    if order.is_offline:
        recipient = 'Offline Pickup'
    else:
        recipient = 'Express Delivery'

    data={
            "first": {"value":title},
            "keyword1":{
                "value":order.classified.title,"color":color
            },
            "keyword2":{
                "value":f'{order.classified.price} RMB',"color":color
            },
            "keyword3":{
                "value":recipient,"color":color
            },
            "keyword4":{
                "value":order.buyer.username,"color":color
            },
            "keyword5":{
                "value":order.buyer.city,"color":color
            },
            "remark": {"value":tail}
        }

    logging.error(
        f'Failed to notify seller on Classified Order',
        extra=data
    )

    wx_push.do_push(classified.user.userid, template_id, url, color, data)
