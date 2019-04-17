#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/3 13:59
# @Author  : ruihuancao@gmail.com
# @File    : delete.py
# @Software: PyCharm
import requests


response = requests.get("http://192.168.1.186:8080/api/poetry/list")

print(response.text)
