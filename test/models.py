#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/7/2018 10:24 AM
# @Author  : ruihuancao@gmail.com
# @File    : models.py
# @Software: PyCharm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import datetime

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:caoruihuan@localhost/poetry_test?charset=utf8"
ModeBase = declarative_base()


class Author(ModeBase):
    """
    作者表
    """
    __tablename__ = "poetry_author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    info = Column(Text)
    dynasty = Column(String(200))
    pic = Column(String(300))
    like_num = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class AuthorInfo(ModeBase):
    """
    作者详细信息表
    """
    __tablename__ = "poetry_author_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer)
    title = Column(String(200))
    info = Column(Text)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class Poetry(ModeBase):
    """
    诗文信息
    """
    __tablename__ = "poetry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300))
    author = Column(String(200))
    author_id = Column(Integer)
    dynasty = Column(String(200))
    content = Column(Text)
    tag = Column(Text)
    like_num = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


class PoetryTranslation(ModeBase):
    """
    译文
    """
    __tablename__ = "poetry_translation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(Text)
    content = Column(Text)
    poetry_id = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow())


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
ModeBase.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# now all calls to Session() will create a thread-local session

class DBManager(object):

    def close_session(self):
        self.session.close()

    def exist_author(self, name):
        ret = self.session.query(Author).filter(Author.name == name).count()
        return ret > 0

    def add_author(self, author):
        if self.exist_author(author.name):
            print("已经存在")
        else:
            self.session.add(author)
            self.session.commit()


