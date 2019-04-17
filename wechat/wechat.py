#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 16:41
# @Author  : ruihuancao@gmail.com
# @File    : wechat.py
# @Software: PyCharm

import itchat
from tuling import TuLing

api_key = 'ae7a8a0e37374ce8ad175f4398a6fe8b'
tuling_robot = TuLing(key=api_key, userId="test")


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    print(msg)
    defaultReply = 'I received: ' + msg['Text']
    if msg['FromUserName'] == '@e4dd212eacc48d54d8d39cb05fe5c5a8':
        reply = tuling_robot.get_response(msg['Text'])
        return reply
    print(defaultReply)

itchat.auto_login(hotReload=True)
itchat.run()
