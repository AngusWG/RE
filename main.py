#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
"""整个系统的主入库"""
# from kivy.app import App
# from kivy.uix.label import Label
from pprint import pprint

from bin.log import log
from bin.server import Server


#
# class MyApp(App):
#     def __init__(self, **kwargs):
#         self.server = Server(log())
#         super().__init__(**kwargs)
#
#     def build(self):
#         return Label(text='Hello world')
#
#
# def main_by_ui():
#     MyApp().run()


def main_by_command():
    server = Server(log())
    film_list = []
    while True:
        film_name = input("请输入电影名称(按1结束)\n：")
        if film_name == "1":
            break
        print("请等待")
        x = server.film_name_list(film_name)
        for i, n in enumerate(x):
            print(i + 1, n["name"])
        film_list.append(x[int(input("请输入编号进行选择\n:")) - 1])
    analysis_type = input("请输入你想查找的方式：\n1 内容推荐\n2 品味推荐\n:")
    if analysis_type not in "12":
        print("输入错误")
        return
    arg = [i["_id"] for i in film_list]
    res = server.same_attributes(*arg) if analysis_type == "1" else server.same_taste(*arg)
    pprint(res)


if __name__ == '__main__':
    main_by_command()
    ####
    # 爬虫
    # do()
    pass
