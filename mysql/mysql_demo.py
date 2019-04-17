#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 17:36
# @Author  : ruihuancao@gmail.com
# @File    : mysql_demo.py
# @Software: PyCharm



from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:caoruihuan@localhost/test?charset=utf8"

ModeBase = declarative_base()

class HtmlData(ModeBase):
    __tablename__ = "html_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200))
    content = Column(Text)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


def savehtml(html):
    session = DBSession()
    session.add(html)
    session.commit()
    session.close()

def savehtmls(htmls):
    session = DBSession()
    session.add_all(htmls)
    session.commit()
    session.close()

def toFile(name, content):
    f = open("%s.json" % name, "w")
    f.write(content)
    f.close()

def sqlToJson(num):
    session = DBSession()
    count = session.query(HtmlData).count()
    block = count//num
    current = 0
    index = 0
    for i in range(num):
        if (i + 1 == num):
            index = count
        else:
            index = index + block
        results = session.query(HtmlData).filter(HtmlData.id > current, HtmlData.id <= index)
        content = []
        for result in results:
            content.append(result.to_json())
        data = {
            "results" : content
        }
        json_result = json.dumps(data)
        toFile(i, json_result)
        current = index


if __name__ == "__main__":
    """
    python sqlalchemy mysql 自动建立表
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    ModeBase.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    sqlToJson(5)


