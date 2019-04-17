#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/8/2018 2:24 PM
# @Author  : ruihuancao@gmail.com
# @File    : testthread.py
# @Software: PyCharm
from util.thread_utils import QueueThread, Task


test = QueueThread()
test.init(5)

for i in range(4000):
    task = Task(name="task-%d" %(i), data="")
    test.add_task(task)

test.end()