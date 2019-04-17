#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/8/2018 4:49 PM
# @Author  : ruihuancao@gmail.com
# @File    : api_test.py
# @Software: PyCharm

import requests

def test_login(username, password):
    url = 'http://localhost:8080/api/auth/login'
    data = {
        "username" : username,
        "password" : password
    }
    response = requests.post(url, data)
    return response.json()

def test_register(username, password, email):
    url = 'http://localhost:8080/api/auth/register'
    data = {
        "username" : username,
        "password" : password,
        "email": email
    }
    response = requests.post(url, data)
    return response.json()

def test_user_list(token):
    url = 'http://localhost:8080/api/user/list'
    headers = {
        "token" : token,
        'Accept':'text/html'
    }
    response = requests.get(url, headers=headers)
    return response.text

def test_user_info(token):
    url = 'http://localhost:8080/api/user/admin'
    headers = {
        "token" : token,
    }
    response = requests.get(url, headers=headers)
    return response.text

if  __name__ == "__main__":

    # username = "caoruihuan"
    # password = "caoruihuan"
    # email = "caoruihuan@gmail.com"
    # response  = test_register(username, password, email)
    # print(response)
    # print("注册成功")
    # response = test_login(username, password)
    # print(response)
    # print("登陆成功")
    # token = response["data"]["token"]
    # response = test_user_list(token)
    # print(response)
    # print("获取失败")

    response = test_login("admin", "admin")
    print(response)
    print("登陆成功")
    token = response["data"]["token"]
    response = test_user_info(token)
    print(response)
    print("获取成功")

    response = test_login("client", "client")
    print(response)
    print("登陆成功")
    token = response["data"]["token"]
    response = test_user_info(token)
    print(response)
    print("获取成功")

