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


def test233():
    server = Server(log())

    res = ["她 Her (2013)",
           "怦然心动", "小情人", "初恋这件小事", "宝贝老板", "爱宠大机密", "香肠派对", "欢乐好声音", "冰雪奇缘", "无敌破坏王",
           "疯狂动物城"]
    arg = []
    print("开始搜索")
    for i in res:
        film =server.film_name_list(i)[0]
        print("获得{}的数据".format(film["name"]))
        arg.append(film["_id"])
    pprint(server.same_taste(*arg))

    ##########################
    # file0 = server.film_name_list("无间道")[0]
    # file1 = server.film_name_list("禁闭岛")[0]
    # file2 = server.film_name_list("触不可及")[0]
    # print(file0, file1, file2)
    # pprint(server.same_taste("26311973"))
    # a = server.find_films_by_tag("感人")
    # print(server.user_info("62457534"))
    # print(a)
    # print(len(set([i.get("_id") for i in a])))




if __name__ == '__main__':
    # main_by_command()
    test233()
    ####
    # 爬虫
    # do()
    pass
