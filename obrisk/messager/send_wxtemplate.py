#!/usr/bin/env python
#-*- coding:utf-8 -*-

from urllib.request import urlopen
import json
import logging
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
        content = self.post_data(request_url + token, json_template)
        #读取json数据
        j = json.loads(content)
        j.keys()

        if j['errcode'] != 0:
            logging.error(
                    'Pushing Wx Template failed',
                    extra={'response': j}
                )


def unread_msgs_wxtemplate(userid, sender, last_msg):
    wx_push = WechatPush()
    template_id = "8un0scoGsT6XKQkm0sMPXqj8WngXfW7YBbPp4KoIz6U"
    url = "https://www.obrisk.com/ws/messages/?dd=" + userid

    color = "#1faece"
    title = "Hi you have received new messages, Open the app to view them"
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
                "value":"Unread messages","color":color
            },
            "remark": {"value":tail}
        }

    wx_push.do_push(userid,template_id,url,color,data)
