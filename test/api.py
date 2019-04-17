#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/8/2018 10:35 AM
# @Author  : ruihuancao@gmail.com
# @File    : api.py
# @Software: PyCharm
import requests

from .models import Author, AuthorInfo, Poetry, PoetryTranslation


class Gushi(object):
    """
    古诗文网请求解析
    """

    headers = {
        'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; MI 5X MIUI/V9.5.3.0.NDBCNFA)'
    }

    def get_author_info(self, id):
        """
        获取作者详细信息
        :param id: 作者id
        :return:
        """
        url = "https://app.gushiwen.org/api/author/author.aspx"
        data = {
            "id": id,
            "token": "gswapi"
        }
        response = requests.post(url, data, self.headers)
        return response.json()

    def get_author(self, page=1):
        """
        获取作者列表
        :param page: page
        :return:
        """
        url = 'https://app.gushiwen.org/api/author/Default.aspx'
        data = {
            "p": page,
            "c": "",
            "id": 0,
            "pwd": "",
            "token": "gswapi"
        }
        response = requests.post(url, data, self.headers)
        return response.json()

    def get_author_page(self):
        """
        获取作者列表总页数
        :return:
        """
        json = self.get_author()
        return json["sumPage"]

    def get_author_peotry(self, id, page):
        """
        获取作者诗文列表
        :param id: 作者id
        :param page: 当前页面
        :return:
        """
        url = "https://app.gushiwen.org/api/author/authorsw.aspx"
        data = {
            "id": id,
            "page": page,
            "token": "gswapi"
        }
        response = requests.post(url, data, self.headers)
        print("response:", response.text)
        return response.json()

    def get_peotry_translation(self, id):
        """
        获取诗文翻译
        :param id: 诗文id
        :return:
        """
        url = "https://app.gushiwen.org/api/shiwen/ajaxshiwencont.aspx"
        data = {
            "id": id,
            "value": "yi",
            "token": "gswapi"
        }
        response = requests.post(url, data, self.headers)
        print("response:", response.text)
        return response.json()

    def get_author_peotry_page(self, id):
        json = self.get_author_peotry(id, 1)
        print(json)
        return json["sumPage"]

    def parse_author(self, json):
        authors = []
        author_ids = []
        for author in json['authors']:
            name = author["nameStr"]
            desc = author["cont"]
            dynasty = author["chaodai"]
            pic_name = author["pic"]
            if (bool(pic_name)):
                pic = "https://img.gushiwen.org/authorImg/" + pic_name + ".jpg"
            else:
                pic = ""
            likes = author["likes"]
            author_id = author["id"]
            author_data = Author(name=name, info=desc, dynasty=dynasty, pic=pic, like_num=likes)
            authors.append(author_data)
            author_ids.append(author_id)
        return authors, author_ids

    def parse_peoty(self, json, author_id):
        poetry_list = []
        poetry_ids = []
        for poetry_json in json["tb_gushiwens"]:
            name = poetry_json["nameStr"]
            content = poetry_json["cont"]
            author = poetry_json["author"]
            dynasty = poetry_json["chaodai"]
            likes = poetry_json["exing"]
            tag = poetry_json["tag"]
            id = poetry_json["id"]
            poetry = Poetry(name=name, author=author, dynasty=dynasty,
                            content=content, author_id=author_id,
                            like_num=likes, tag=tag)
            poetry_list.append(poetry)
            poetry_ids.append(id)
        return poetry_list, poetry_ids

    def parse_author_info(self, json, author_id):
        info_json_list = json["tb_ziliaos"]["ziliaos"]
        info_list = []
        for info_json in info_json_list:
            title = info_json["nameStr"]
            info = info_json["cont"]
            author_info = AuthorInfo(title=title, info=info, author_id=author_id)
            info_list.append(author_info)
        return info_list

    def parse_peotry_translation(self, json, poetry_id):
        reference = json["cankao"]
        content = json["cont"]
        if bool(content):
            poetry_translation = PoetryTranslation(reference=reference, content=content, poetry_id=poetry_id)
            return poetry_translation
        else:
            return None
