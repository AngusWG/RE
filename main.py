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
    crawler = Crawler(100, 30, l)
    # user_id = crawler.film_review_list("6722879")
    # print(len(set(user_id)), user_id)
    print(crawler.film_info_by_id("6722879"))
    # print(crawler.film_info_by_name("她"))
    # print(crawler.film_list_by_name("她"))
    # print(crawler.same_tag_list("黑帮"))


def test_server():
    server = Server(log())
    #######################
    arg = server.films_by_user('52357979')
    arg = [i for i in arg[:2]]
    film_list = server.same_taste(*arg)
    for i in film_list:
        print("\n推荐电影：" + i["name"])
        print("电影连接：" + "https://movie.douban.com/subject/" + i["_id"])
    print(film_list)
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


def test_one(user_id):
    server = Server(log())
    arg = server.films_by_user(user_id)
    user_like = arg
    arg = arg[:15]
    same_attributes = [i["_id"] for i in server.same_attributes(*arg)]
    same_taste = [i["_id"] for i in server.same_taste(*arg)]
    same_taste = []
    a = b = 0
    for film_id in same_attributes:
        if film_id in user_like:
            a += 1
    for film_id in same_taste:
        if film_id in user_like:
            b += 1
    return a / 15, b / 15


def test_app():
    user_list = ['60016273', 'chabbytong', 'nezhaboy', 'Alex-boil', '29725427', '1577696', 'linlyland', 'nyse',
                 '2468214', '155538609', '33360599', '72985710', 'yuyang1990720', 'CRA1G', 'Gordoncoco', 'joesai',
                 '76879186', 'rubbitU', 'christinett', '41635980', 'michicody', '56492265', '75672989', '150806470',
                 'littleruo', 'young753951', '3574182', 'sunakiko', '168068566', 'hooded_cat', 'pengpeng9527',
                 '132087897', '85452483', '42282373', 'vcisemo', '64243172', '154274861', 'azuresing', 'postr',
                 '57989852', '97646535', 'myronlau', 'yyqy', '3319180', '53822613', '4481826', 'tuzichiluobo',
                 'Why-Iam-Myself', 'cuisandy', '56128139', '66813250', '144945517', '1322481', '94818931', '122147852',
                 '3330680', 'shenzixu', 'zoujian-999', '2081187', 'kinna', '172036880', '145978414', 'icicle0226',
                 'duduxiongzhifu', 'JosephineQv', '41835913', 'martinchen', '121490926', '54946053', 'lolitalempick',
                 '153538783', '150577380', '156675491', 'evaplechu', '2004382', 'autumnlynn', '35224934', '57087441',
                 '1644844', '130693126', '2685340', 'dgzy1644', '121153317', 'weneedcookie', 'Gardenialost',
                 'Tiamo0118', 'tjz230', '48996305', '35288569', '55627956', 'vanelevel', '2003525', '62236849',
                 '2837777', 'Neko-', '2224035', '82922427', 'angelazha', 'muamu913', '71461134', 'baby-t', '44532870',
                 '45518242', '173677150', '131922601', 'QueenGround', '42235195', 'shoegazerbaby', '153094408',
                 'SM0916', '51177363', '4195001', '148187682', '72261882', 'Just_vv', 'afratop', '151871851',
                 'YeonParadise', '30091624', 'narreterpas', 'Esperanzatino', 'lintao', 'viviansu', '34031274',
                 '127317129', 'yhming', 'Pikachu1127', '2805103', '2357024', 'amridsl', 'salim', 'weiweilo5e',
                 'vero_nicat', '157087384', '145944151']
    a, b = 0, 0
    user_list = user_list[:30]
    print(user_list)
    for i in user_list:
        same_attributes, same_taste = test_one(i)
        a += same_attributes
        b += same_taste
    print("same_attributes :", a / len(user_list) * 100, "%")
    print('same_taste:', b / len(user_list) * 100, "%")


if __name__ == '__main__':
    # main_by_command()
    # test_crawler()
    test_server()
    # test_app()
    ####
    # 爬虫
    # do()
    pass
