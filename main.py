#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
"""整个系统的主入库"""
# from kivy.app import App
# from kivy.uix.label import Label
from pprint import pprint

from bin.crawler import Crawler
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


def test_crawler():
    l = log()
    crawler = Crawler(100, 100, l)
    user_id = crawler.film_review_list("6722879")
    print(len(set(user_id)), user_id)
    print(crawler.film_info_by_id(1315316))
    print(crawler.film_info_by_name("她"))
    print(crawler.film_list_by_name("她"))
    print(crawler.same_tag_list("黑帮"))


def test_server():
    server = Server(log())
    #######################
    arg = server.films_by_user('52357979')
    arg = [i["_id"]for i in arg]
    film_list = server.same_attributes(*arg)
    for i in film_list:
        print("\n推荐电影：" + i["name"])
        print("电影连接：" + "https://movie.douban.com/subject/" + i["_id"])

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
    # test_crawler()
    test_server()
    ####
    # 爬虫
    # do()
    pass
