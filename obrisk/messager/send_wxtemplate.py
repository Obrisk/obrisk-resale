#!/usr/bin/env python
#-*- coding:utf-8 -*-

from urllib.request import urlopen
import json
import logging
import requests
from obrisk.utils.wx_config import get_access_token


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
        logging.error(f'Testing the response', extra={'response': response})
        j = response.json()
        j.keys()

        if j['errcode'] != 0:
            logging.error(
                    'Pushing Wx Template failed',
                    extra={'response': j}
                )


def unread_msgs_wxtemplate(userid, sender, last_msg):
    wx_push = WechatPush()
    template_id = "NRK2BaSoEtf7SRImLTddE4EqzZvu4Lry84Yfh3Of_Kc"
    url = "https://www.obrisk.com/ws/messages/?dd=" + userid

    color = "#173177"
    title = "Hi you have received new messages, Open the app to view them"
    tail = "Thank you for using Obrisk"

    data={
            "first": {"value":title},
            "keyword1":{
                "value":sender,"color":color
            },
            "keyword2":{
                "value":last_msg,"color":color
            },
            "keyword3":{
                "value":"22:11 20-July-21","color":color
            },
            "keyword4":{
                "value":"Please reply ASAP","color":color
            },
            "remark": {"value":tail}
        }

    wx_push.do_push(userid,template_id,url,color,data)
