#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/8/2018 10:46 AM
# @Author  : ruihuancao@gmail.com
# @File    : gushiv2.py
# @Software: PyCharm

from test.api import Gushi

from test.models import *
from util.thread_utils import QueueThread, Task
import time


class GushiThread(QueueThread):

    def progress_task(slef, task):
        try:
            net_id = task.data["net_id"]
            id = task.data["db_id"]
            session = Session()
            # 获取作者详细信息
            author_info_json = gushi.get_author_info(id=net_id)
            print("获取到作者", id, "的信息")
            author_info = gushi.parse_author_info(json=author_info_json, author_id=id)
            session.add_all(author_info)
            session.commit()
            print("保存作者", id, "的信息")
            time.sleep(1)
            # 获取作者诗文
            poetry_page = 1
            poetry_page_count = gushi.get_author_peotry_page(net_id)
            print("获取作者的诗词列表总页数：", poetry_page_count)
            while poetry_page < (poetry_page_count + 1):
                print("获取作者", id, "的第", poetry_page, "页诗词")
                poetry_page += 1
                try:
                    poetry_json = gushi.get_author_peotry(id=net_id, page=poetry_page)
                    poetry_list, poetry_ids = gushi.parse_peoty(poetry_json, id)
                    session.add_all(poetry_list)
                    session.commit()
                except (Exception):
                    continue
                print("保存作者", id, "的第", poetry_page, "页的诗词")
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
                        continue
                    print("保存诗文", poetry_id, "的译文")
            print("作者：", id, "的作品获取完毕")
        except Exception:
            print("异常跳过")

if __name__ == "__main__":
    gushi = Gushi()
    gushi_thread = GushiThread()
    gushi_thread.init(work_thread_num=10)
    page_count = gushi.get_author_page()
    session = Session()
    page = 1
    page_count = 1
    print("page count:", page_count)
    while page < (page_count + 1):
        try:
            author_json = gushi.get_author(page)
            print("获取到第", page, "页作者列表:")
            print(author_json)
            authors, author_ids = gushi.parse_author(json=author_json)
            session.add_all(authors)
            session.commit()
            print("保存第", page, "页作者列表")
            i = 0
            while i < len(authors):
                net_id = author_ids[i]
                id = authors[i].id
                data = {
                    "db_id": id,
                    "net_id": net_id
                }
                task = Task(name="task-%d" % i, data=data)
                gushi_thread.add_task(task)
                i += 1
            time.sleep(10)
        except Exception:
            print("异常跳过")
            continue
        page += 1
    Session.remove()
    gushi_thread.end()
