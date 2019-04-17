#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 17:17
# @Author  : ruihuancao@gmail.com
# @File    : tuling.py
# @Software: PyCharm
import requests
import json


class TuLing:
    open_url = 'http://openapi.tuling123.com/openapi/api/v2'

    def __init__(self, key, userId):
        self.key = key
        self.userId = userId

    def get_response(self, msg):
        try:
            input_text = {'text': msg}
            user_info = {'apiKey': self.key, 'userId': self.userId}
            perception = {'inputText': input_text}
            data = {'perception': perception, 'userInfo': user_info}
            response = requests.post(url=self.open_url, data=json.dumps(data))
            response.encoding = 'utf-8'
            result = response.json()
            print(result)
            # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
            return result['results'][0]['values']['text']
        except:
            # 将会返回一个None
            return

if __name__ == '__main__':
    api_key = 'ae7a8a0e37374ce8ad175f4398a6fe8b'
    tuling_rebot = TuLing(key=api_key, userId="1")
    print(tuling_rebot.get_response(msg="西安天气？"))
