#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
import pymongo


class DBUtils:
    def __init__(self):
        self.db = pymongo.MongoClient("127.0.0.1", 27017)["RE"]

    def file_info(self):
        """获取一部电影的信息"""
        pass

    def file_name_list(self):
        """搜索数据库中电影的名字集，结果多于X条返回None，名字错误返回False，"""
        pass

    def DB_check(self):
        pass
