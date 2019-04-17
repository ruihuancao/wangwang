#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/13 14:04
# @Author  : ruihuancao@gmail.com
# @File    : movie.py
# @Software: PyCharm

import requests

#url = "http://m.dydytt.net:8080/adminapi/api/movieList.json?categoryId=2&page=1&searchContent="
url = "https://okzyw.com/index.php?m=vod-search"
# x-header-request-timestamp: 1531461616
# x-header-request-imei:
# x-header-request-key: 4725d3a579eb072ab330a97120ee57fa
# Host: m.dydytt.net:8080
# Connection: Keep-Alive
# Accept-Encoding: gzip
# User-Agent: okhttp/3.8.0

# headers = {
#     "User-Agent" :"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
# }
#
# data = {
#     "wd":"华尔街",
#     "submit":"search"
# }
# response  = requests.post(url=url, headers=headers, data=data)
# print(response.text)

response = requests.get(url="https://okzyw.com/?m=vod-type-id-1.html")
print(response.text)
