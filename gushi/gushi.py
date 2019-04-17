#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/6/2018 4:07 PM
# @Author  : ruihuancao@gmail.com
# @File    : gushi.py
# @Software: PyCharm
import requests
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:caoruihuan@localhost/gushiwen_normal?charset=utf8"
ModeBase = declarative_base()


class Author(ModeBase):
    """
    作者表
    """
    __tablename__ = "gushi_author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    desc = Column(Text)
    dynasty = Column(String(200))
    pic = Column(String(300))
    likes = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class AuthorInfo(ModeBase):
    """
    作者详细信息表
    """
    __tablename__ = "gushi_author_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer)
    title = Column(String(200))
    info = Column(Text)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class Poetry(ModeBase):
    """
    诗文信息
    """
    __tablename__ = "gushi_poetry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300))
    author = Column(String(200))
    author_id = Column(Integer)
    dynasty = Column(String(200))
    content = Column(Text)
    tag = Column(Text)
    likes = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class PoetryTranslation(ModeBase):
    """
    译文
    """
    __tablename__ = "gushi_poetry_translation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(Text)
    content = Column(Text)
    poetry_id = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class Gushi(object):
    """
    古诗文网请求解析
    """

    headers = {
        'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; MI 5X MIUI/V9.5.3.0.NDBCNFA)'
    }

    def __init__(self, name):
        self.name = name

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
            author_data = Author(name=name, desc=desc, dynasty=dynasty, pic=pic, likes=likes)
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
                            likes=likes, tag=tag)
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


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    ModeBase.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    gushi = Gushi("gushi")
    # 1 获取作者列表总页数
    page_count = gushi.get_author_page()
    print("获取作者列表总数：", page_count)
    # 2 获取所有作者
    page = 1
    time.sleep(1)
    while page < (page_count + 1):
        try:
            author_json = gushi.get_author(page)
            print("获取到第", page, "页作者列表")
            authors, author_ids = gushi.parse_author(json=author_json)
            session.add_all(authors)
            session.commit()
            print("保存第", page, "页作者列表")
        except(Exception):
            print("异常跳过")
            page += 1
            continue
        time.sleep(1)

        # 获取作者详细信息
        i = 0;
        while i < len(authors):
            net_id = author_ids[i]
            id = authors[i].id
            # 获取作者详细信息
            try:
                author_info_json = gushi.get_author_info(id=net_id)
                print("获取到作者", id, "的信息")
                author_info = gushi.parse_author_info(json=author_info_json, author_id=id)
                session.add_all(author_info)
                session.commit()
                print("保存作者", id, "的信息")
            except(Exception):
                print("异常跳过")
                session.rollback()
                i += 1
                continue
            time.sleep(1)
            i += 1
            # 获取作者诗文
            poetry_page = 1
            poetry_page_count = gushi.get_author_peotry_page(net_id)
            print("获取作者的诗词列表总页数：", poetry_page_count)
            while poetry_page < (poetry_page_count + 1):
                print("获取作者", id, "的第", poetry_page, "页诗词")
                try:
                    poetry_json = gushi.get_author_peotry(id=net_id, page=poetry_page)
                    poetry_list, poetry_ids = gushi.parse_peoty(poetry_json, id)
                    session.add_all(poetry_list)
                    session.commit()
                except (Exception):
                    print("异常跳过")
                    poetry_page += 1
                    continue
                print("保存作者", id, "的第", poetry_page, "页的诗词")
                poetry_page += 1
                time.sleep(1)

                # 获取诗文的译文
                j = 0
                while j < len(poetry_ids):
                    poetry_net_id = poetry_ids[j]
                    poetry_id = poetry_list[j].id
                    j += 1
                    try:
                        poetry_translation_json = gushi.get_peotry_translation(poetry_net_id)
                        poetry_translation = gushi.parse_peotry_translation(json=poetry_translation_json,
                                                                            poetry_id=poetry_id)
                        if bool(poetry_translation):
                            session.add(poetry_translation)
                            session.commit()
                        else:
                            print("诗文翻译为空")
                    except (Exception):
                        print("异常跳过")
                        continue
                    print("保存诗文", poetry_id, "的译文")
            print("作者：", id, "的作品获取完毕")
        page += 1
        print("第", page, "的作者及作品获取完毕")
    session.close()
    print("抓取结束")
