#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/29 10:00
# @Author  : ruihuancao@gmail.com
# @File    : lovemuyi.py
# @Software: PyCharm


from aip import AipOcr
import os
from decimal import Decimal
from tkinter import *
from tkinter.filedialog import askdirectory
import threading
import tkinter.messagebox as messagebox
import re
import sys
import shutil
import time

""" 你的 APPID AK SK
打包命令：
pyinstaller -i icon.ico -F lovemuyi.py --noconsole
"""
APP_ID = '10681084'
API_KEY = 'DFMYlWq4ZHx3HZWs4xs7tNRY'
SECRET_KEY = 'o9p5yKL6szthRDuyaKakQr11qGXPmyYd'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
templateSign = "e19e3b3c1f8354c3d6ab184bb29d5f44"

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_image_info(image_path):
    image = get_file_content(image_path)
    """ 调用自定义模版文字识别 """
    response = client.custom(image, templateSign)
    print(response['data']['ret'])
    return parase(response['data'])


def parase(data):
    parase_data = {}
    for item in data['ret']:
        value = item['word']
        name = item['word_name']
        parase_data[name] = value
    return parase_data

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=X)
        self.select_path = './image/'
        self.message = ''
        self.createWidgets()
        self.is_calculation = False

    def createWidgets(self):
        self.selectButton = Button(self, text='选择目录', command=self.select_dir)
        self.calculationButton = Button(self, text='开始计算', command=self.calculation)
        self.clearButton = Button(self, text='日志清理', command=self.clear)
        self.selectButton.pack(fill=X)
        self.calculationButton.pack(fill=X)
        self.clearButton.pack(fill=X)
        self.infoText = Text(self,width = 100, height=200)
        self.infoText.pack(fill=X)

    def select_dir(self):
        if self.is_calculation:
            messagebox.showinfo('提示', "亲爱的，正在计算，请稍后...")
        else:
            self.select_path = askdirectory()
            self.add_message("选择目录：%s" % self.select_path)


    def add_message(self, info):
        text = info+ "\n"
        self.infoText.insert(END, text)

    def calculation(self):
        if self.is_calculation:
            messagebox.showinfo('提示', "亲爱的，正在计算，请稍后...")
        else:
            CalculationThread(self.start_calculation).start()

    def clear(self):
        self.infoText.delete(0.0, END)

    def start_calculation(self):
        self.is_calculation = True
        try:
            self.clear()
            self.add_message("开始识别...")
            images = os.listdir(self.select_path)
            count_num = 0
            error_path = []
            result = {}
            image_path = ""
            all_image = 0
            for image in images:
                if((not (image.endswith(".jpg")
                         or image.endswith(".png")
                         or image.endswith(".PNG")
                         or image.endswith(".JPG")
                         )
                    )
                   ):
                    print(image, "文件跳过")
                    self.add_message("不支持文件:%s" % image)
                    continue
                all_image+=1
                try:
                    image_path = self.select_path + "/" + image
                    self.add_message("正在识别图片:%s" % image_path)
                    data = get_image_info(image_path)
                    self.add_message("%s在%s给%s发了一个%s的红包" % (data['send_name'],
                                                            data['receive_time'],
                                                            data['receive_name'],
                                                            data['num']))
                    image_num_str = data['num']
                    image_num_str = re.findall(r"\d+\.?\d*", image_num_str)[0]
                    print(image_num_str)
                    image_num = Decimal(image_num_str).quantize(Decimal('0.00'))
                    if image_num == 0 or image_num > 200:
                        error_path.append(image_path)
                        continue
                    else:
                        result[image_path] = image_num_str
                except Exception:
                    error_path.append(image_path)
                    continue
                count_num += image_num
            self.clear()
            self.add_message("--------------------计算结果---------------------------")
            self.add_message("目录%s下共有截图文件（.jpg）%d张" %(self.select_path, all_image))
            if len(error_path) > 0:
                self.add_message("--------无法识别%d张图片,以下为无法识别文件---------" %(len(error_path)))
                error_file_path = self.select_path +"/error/"
                if os.path.exists(error_file_path):
                    shutil.rmtree(error_file_path)  # 空目录、有内容的目录都可以删
                os.mkdir(error_file_path)
                for path in error_path:
                    shutil.copy(path, error_file_path)
                    self.add_message(path)

            self.add_message("----------以下为成功识别的%d张图片及金额-------" %(len(result)))
            print(result)
            for key, value in result.items():
                self.add_message(key + ' --------' + value)
            self.add_message("成功识别%d张总金额:%s" % (len(result), count_num))
            if len(result) == images:
                self.add_message("成功识别全部。。。")
            else:
                self.add_message("识别失败%d张图片，请手动计算。。。" %(len(error_path)))
            self.is_calculation = False
        except Exception:
            self.is_calculation = False
            print(sys.exc_info())
            self.add_message("计算出错，请重试。。。")


class CalculationThread (threading.Thread):

    def __init__(self, start_calculation):
        threading.Thread.__init__(self)
        self.start_calculation = start_calculation

    def run(self):
        print ("开始线程：" + self.name)
        self.start_calculation()
        print ("退出线程：" + self.name)

app = Application()
current_time = time.strftime("%Y%m%d%H%M", time.localtime())

# 设置窗口标题:
app.master.title('微信红包金额统计%s' % current_time)

# 主消息循环:
app.mainloop()



