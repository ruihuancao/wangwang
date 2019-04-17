#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/8/2018 10:50 AM
# @Author  : ruihuancao@gmail.com
# @File    : threadtest.py
# @Software: PyCharm

import queue
import threading
import time

queueLock = threading.Lock()
workQueue = queue.Queue()
exitFlag = 0


class ProcessTaskThread(threading.Thread):
    """
    任务处理线程
    """

    def __init__(self, name, fun):
        threading.Thread.__init__(self)
        self.name = name
        self.fun = fun

    def run(self):
        print("start thread:", self.name)
        global workQueue
        global exitFlag
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                task = workQueue.get()
                queueLock.release()
                self.fun(task)
            else:
                print("wait progress...")
                queueLock.release()
                time.sleep(1)
        print("end thread:", self.name)


class Task(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class QueueThread(object):
    def init(self, work_thread_num = 3):
        for task in range(work_thread_num):
            thread = ProcessTaskThread("task %d" % task, self.progress_task)
            thread.start()

    def add_task(self, task):
        global workQueue
        global queueLock
        if workQueue.full():
            print("队列已满，等待处理")
        else:
            queueLock.acquire()
            workQueue.put(task)
            print("添加任务，队列总任务数量：%d" % (workQueue.qsize()))
            queueLock.release()

    def end(self):
        global workQueue
        global exitFlag
        # 等待队列清空
        while not workQueue.empty():
            print("等待队列清空")
            time.sleep(1)
        exitFlag = 1
        print("退出主线程")

    def progress_task(slef, task):
        print(" test method processing %s" % (task.name))
        time.sleep(1)

    # if __name__ == "__main__":
    #     start = time.time()
    #     queueThread = TestThread()
    #     task_id = 1
    #     while task_id < 20:
    #         task = Task(name="task", data=task_id)
    #         queueThread.add_task(task)
    #         task_id += 1
    #
    #     queueThread.end()
    #     print(time.time()-start)

    ## 创建新线程
    # for task in range(workThreadNum):
    #     thread = ProcessTaskThread("task %d" % task, test)
    #     thread.start()
    #
    # task_id = 1
    # while task_id < 40:
    #     if workQueue.full():
    #         print("队列已满，等待处理")
    #         time.sleep(1)
    #     else:
    #         queueLock.acquire()
    #         data = "task %d" % (task_id)
    #         workQueue.put(data)
    #         task_id += 1
    #         print("添加任务，队列总任务数量：%d" % (workQueue.qsize()))
    #         queueLock.release()
    #
    # # 等待队列清空
    # while not workQueue.empty():
    #     print("等待队列清空")
    #     time.sleep(1)
    #
    # exitFlag = 1
    # print("退出主线程")
